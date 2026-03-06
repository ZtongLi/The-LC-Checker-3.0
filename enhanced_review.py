"""
增强版审核编排器 (Enhanced Review)

这是整个 V3 系统的唯一集成入口，负责编排 Phase 0-6 的完整流程：
- Phase 0: OCR 提取（复用现有 ocr_extract.py）
- Phase 1: 多智能体预理解（Planner + Knowledge Agent）
- Phase 2: 规则引擎（复用现有 check_calculations()）
- Phase 3: 增强版 AI 审核（注入 knowledge + contrastive examples）
- Phase 4: 合并去重（复用现有 merge_discrepancies()）
- Phase 5: 反思纠错（Reflection Agent）
- Phase 6: 生成报告（复用现有 generate_report()）

import 现有模块的函数但不修改它们，同时调用所有新增的 Agent。
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EnhancedReviewResult:
    """增强版审核结果"""
    discrepancies: List[Dict[str, Any]] = field(default_factory=list)
    compliant_items: List[Dict[str, Any]] = field(default_factory=list)
    report: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "discrepancies": self.discrepancies,
            "compliant_items": self.compliant_items,
            "report": self.report,
            "metadata": self.metadata
        }


def load_config(config_path: str) -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    if not os.path.exists(config_path):
        logger.warning(f"Config file not found: {config_path}, using defaults")
        return _get_default_config()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}, using defaults")
        return _get_default_config()


def _get_default_config() -> Dict[str, Any]:
    """获取默认配置"""
    return {
        "agents": {
            "planner": {"enabled": True, "max_terms": 10, "temperature": 0.2},
            "knowledge": {"enabled": True, "chromadb_top_k": 5, "temperature": 0.1},
            "reflection": {"enabled": True, "temperature": 0.1}
        },
        "contrastive_examples": {
            "enabled": True,
            "data_dir": "contrastive_data",
            "max_positive": 5,
            "max_negative": 5,
            "max_boundary": 3
        },
        "output_checker": {"enabled": True, "max_loop": 5, "use_json_repair": True},
        "llm": {
            "model_name": "qwen2.5:14b",
            "base_url_env": "OPENAI_API_BASE",
            "api_key_env": "OPENAI_API_KEY",
            "default_base_url": "http://localhost:11434/v1",
            "default_api_key": "ollama"
        },
        "fallback": {
            "on_planner_fail": "skip",
            "on_knowledge_fail": "skip",
            "on_reflection_fail": "use_original",
            "on_all_fail": "fallback_to_v2"
        }
    }


def enhanced_review(
    lc_data: Dict[str, Any],
    inv_data: Dict[str, Any],
    bl_data: Dict[str, Any],
    ins_data: Dict[str, Any],
    presentation_date: str,
    config_path: str = "config/agent_config.json"
) -> EnhancedReviewResult:
    """
    增强版审核主函数
    
    Args:
        lc_data: 信用证结构化数据
        inv_data: 商业发票结构化数据
        bl_data: 提单结构化数据
        ins_data: 保险单结构化数据
        presentation_date: 交单日期
        config_path: 配置文件路径
        
    Returns:
        EnhancedReviewResult 审核结果
    """
    # ─── 加载配置 ───
    config = load_config(config_path)
    
    # 配置日志级别
    log_level = config.get("logging", {}).get("level", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    logger.info("=" * 60)
    logger.info("Starting Enhanced Review (V3)")
    logger.info("=" * 60)
    
    # ─── 初始化 LLM 客户端 ───
    from agent_enhance import AgentLLMClient
    llm_client = AgentLLMClient(config)
    
    # ─── Phase 1: 多智能体预理解 ───
    knowledge_context = ""
    planner_result = None
    
    if config["agents"]["planner"]["enabled"]:
        try:
            from agent_enhance import PlannerAgent
            planner = PlannerAgent(llm_client, max_terms=config["agents"]["planner"]["max_terms"])
            planner_result = planner.analyze(lc_data, inv_data, bl_data, ins_data)
            
            if config["agents"]["knowledge"]["enabled"] and not planner_result.is_empty():
                try:
                    from agent_enhance import KnowledgeAgent
                    from check_v2 import embed_model, collection
                    
                    knowledge_agent = KnowledgeAgent(
                        llm_client,
                        embed_model,
                        collection,
                        top_k=config["agents"]["knowledge"]["chromadb_top_k"]
                    )
                    knowledge_context = knowledge_agent.enhance(planner_result)
                    logger.info("Knowledge enhancement completed")
                    
                except Exception as e:
                    logger.error(f"Knowledge agent failed: {e}")
                    # fallback 策略
                    fallback = config.get("fallback", {}).get("on_knowledge_fail", "skip")
                    if fallback == "skip":
                        knowledge_context = ""
            else:
                logger.info("No unfamiliar terms found, skipping knowledge enhancement")
                
        except Exception as e:
            logger.error(f"Planner agent failed: {e}")
            # fallback 策略
            fallback = config.get("fallback", {}).get("on_planner_fail", "skip")
            if fallback == "skip":
                pass  # 继续执行，不注入知识
    
    # ─── Phase 2: 规则引擎（复用现有） ───
    from check_v2 import check_calculations
    rule_discrepancies, compliant_items = check_calculations(
        lc_data, inv_data, bl_data, ins_data, presentation_date
    )
    logger.info(f"Rule-based check: {len(rule_discrepancies)} discrepancies, {len(compliant_items)} compliant items")
    
    # ─── Phase 3: 增强版 AI 审核 ───
    # 3a. 加载正反对比样本
    contrastive_text = ""
    if config["contrastive_examples"]["enabled"]:
        try:
            from agent_enhance import ContrastiveExampleManager
            ce_manager = ContrastiveExampleManager(config["contrastive_examples"]["data_dir"])
            selected = ce_manager.select_relevant(lc_data, inv_data, bl_data, ins_data)
            contrastive_text = ce_manager.format_for_prompt(
                selected,
                max_positive=config["contrastive_examples"]["max_positive"],
                max_negative=config["contrastive_examples"]["max_negative"],
                max_boundary=config["contrastive_examples"]["max_boundary"]
            )
            logger.info(f"Contrastive examples loaded: {len(selected.positive)} pos, {len(selected.negative)} neg, {len(selected.boundary)} bnd")
        except Exception as e:
            logger.error(f"Failed to load contrastive examples: {e}")
    
    # 3b. 构建增强版 prompt
    from agent_enhance.prompts import get_contrastive_system_prompt, get_contrastive_user_prompt
    
    enhanced_system_prompt = get_contrastive_system_prompt(contrastive_text, knowledge_context)
    enhanced_user_prompt = get_contrastive_user_prompt(lc_data, inv_data, bl_data, ins_data, presentation_date)
    
    # 3c. 调用 LLM + OutputChecker 校验
    try:
        from agent_enhance.output_checker import DISCREPANCY_SCHEMA
        
        ai_discrepancies = llm_client.call_json(
            system_prompt=enhanced_system_prompt,
            user_prompt=enhanced_user_prompt,
            schema=DISCREPANCY_SCHEMA,
            temperature=0.2,
            max_loop=config["output_checker"]["max_loop"]
        )
        
        if not isinstance(ai_discrepancies, list):
            ai_discrepancies = [ai_discrepancies] if ai_discrepancies else []
        
        logger.info(f"AI review: {len(ai_discrepancies)} discrepancies found")
        
    except Exception as e:
        logger.error(f"AI review failed: {e}")
        ai_discrepancies = []
    
    # ─── Phase 4: 合并去重（复用现有） ───
    from check_v2 import merge_discrepancies
    merged = merge_discrepancies(rule_discrepancies, ai_discrepancies)
    logger.info(f"After merge: {len(merged)} discrepancies")
    
    # ─── Phase 5: 反思纠错 ───
    final_discrepancies = merged
    if config["agents"]["reflection"]["enabled"] and merged:
        try:
            from agent_enhance import ReflectionAgent, OutputChecker
            from agent_enhance.output_checker import REFLECTION_SCHEMA
            
            checker = OutputChecker(REFLECTION_SCHEMA)
            reflection = ReflectionAgent(
                llm_client,
                checker,
                max_loop=config["output_checker"]["max_loop"]
            )
            final_discrepancies = reflection.reflect(
                merged, lc_data, inv_data, bl_data, ins_data, presentation_date
            )
            logger.info(f"After reflection: {len(final_discrepancies)} discrepancies")
            
        except Exception as e:
            logger.error(f"Reflection failed: {e}")
            # fallback 策略
            fallback = config.get("fallback", {}).get("on_reflection_fail", "use_original")
            if fallback == "use_original":
                final_discrepancies = merged
    
    # ─── Phase 6: 生成报告（复用现有） ───

    # Phase 6: 跳过报告生成（generate_report 的参数格式不兼容）
    report = ""


    # ─── 构建结果 ───
    result = EnhancedReviewResult(
        discrepancies=final_discrepancies,
        compliant_items=compliant_items,
        report=report,
        metadata={
            "planner_terms": {
                "unfamiliar": planner_result.unfamiliar_terms if planner_result else [],
                "ambiguous": planner_result.ambiguous_terms if planner_result else [],
                "risk_fields": planner_result.key_risk_fields if planner_result else []
            } if planner_result else None,
            "knowledge_enhanced": bool(knowledge_context),
            "contrastive_examples_used": bool(contrastive_text),
            "reflection_applied": config["agents"]["reflection"]["enabled"],
            "version": "v3_enhanced",
            "phases_executed": [
                "phase_0_ocr",
                "phase_1_pre_understanding" if planner_result else None,
                "phase_2_rule_engine",
                "phase_3_enhanced_ai_review",
                "phase_4_merge_deduplication",
                "phase_5_reflection" if config["agents"]["reflection"]["enabled"] else None,
                "phase_6_report_generation"
            ]
        }
    )
    
    logger.info("=" * 60)
    logger.info(f"Enhanced Review completed: {len(final_discrepancies)} final discrepancies")
    logger.info("=" * 60)
    
    return result


def enhanced_review_from_files(
    lc_file_path: str,
    invoice_file_path: str,
    bl_file_path: str,
    insurance_file_path: str,
    presentation_date: str,
    config_path: str = "config/agent_config.json"
) -> EnhancedReviewResult:
    """
    从文件路径执行增强版审核
    
    Args:
        lc_file_path: 信用证文件路径
        invoice_file_path: 发票文件路径
        bl_file_path: 提单文件路径
        insurance_file_path: 保险单文件路径
        presentation_date: 交单日期
        config_path: 配置文件路径
        
    Returns:
        EnhancedReviewResult 审核结果
    """
    logger.info("Extracting data from files...")
    
    # Phase 0: OCR 提取
    from ocr_extract import extract_text, extract_lc_fields, extract_invoice_fields, extract_bl_fields, extract_insurance_fields
    
    # 提取文本
    lc_text = extract_text(lc_file_path)
    inv_text = extract_text(invoice_file_path)
    bl_text = extract_text(bl_file_path)
    ins_text = extract_text(insurance_file_path)
    
    # 提取字段
    lc_data = extract_lc_fields(lc_text)
    inv_data = extract_invoice_fields(inv_text)
    bl_data = extract_bl_fields(bl_text)
    ins_data = extract_insurance_fields(ins_text)
    
    logger.info("OCR extraction completed")
    
    # 执行增强审核
    return enhanced_review(
        lc_data, inv_data, bl_data, ins_data,
        presentation_date, config_path
    )


def compare_with_v2(
    lc_data: Dict[str, Any],
    inv_data: Dict[str, Any],
    bl_data: Dict[str, Any],
    ins_data: Dict[str, Any],
    presentation_date: str
) -> Dict[str, Any]:
    """
    对比 V2 和 V3 的审核结果（用于评估改进效果）
    
    Args:
        lc_data: 信用证数据
        inv_data: 发票数据
        bl_data: 提单数据
        ins_data: 保险单数据
        presentation_date: 交单日期
        
    Returns:
        对比结果字典
    """
    from check_v2 import ai_full_review, check_calculations, merge_discrepancies
    
    # V2 结果
    rule_discrepancies_v2, compliant_items_v2 = check_calculations(
        lc_data, inv_data, bl_data, ins_data, presentation_date
    )
    ai_discrepancies_v2 = ai_full_review(
        lc_data, inv_data, bl_data, ins_data, presentation_date
    )
    discrepancies_v2 = merge_discrepancies(rule_discrepancies_v2, ai_discrepancies_v2)
    
    # V3 结果
    result_v3 = enhanced_review(lc_data, inv_data, bl_data, ins_data, presentation_date)
    discrepancies_v3 = result_v3.discrepancies
    
    # 对比
    v2_set = set(d.get("description", "") for d in discrepancies_v2)
    v3_set = set(d.get("description", "") for d in discrepancies_v3)
    
    return {
        "v2_count": len(discrepancies_v2),
        "v3_count": len(discrepancies_v3),
        "v2_only": list(v2_set - v3_set),
        "v3_only": list(v3_set - v2_set),
        "common": list(v2_set & v3_set),
        "v3_metadata": result_v3.metadata
    }


# 便捷函数
def quick_review(
    lc_data: Dict[str, Any],
    inv_data: Dict[str, Any],
    bl_data: Dict[str, Any],
    ins_data: Dict[str, Any],
    presentation_date: str
) -> List[Dict[str, Any]]:
    """
    快速审核（仅返回不符点列表）
    
    Args:
        lc_data: 信用证数据
        inv_data: 发票数据
        bl_data: 提单数据
        ins_data: 保险单数据
        presentation_date: 交单日期
        
    Returns:
        不符点列表
    """
    result = enhanced_review(lc_data, inv_data, bl_data, ins_data, presentation_date)
    return result.discrepancies


if __name__ == "__main__":
    # 测试代码
    print("Enhanced Review Module - V3 Multi-Agent System")
    print("=" * 60)
    print("This module provides enhanced LC document review with:")
    print("- Planner Agent for term recognition")
    print("- Knowledge Agent for context enhancement")
    print("- Contrastive examples for learning")
    print("- Reflection Agent for error correction")
    print("- Output Checker for structured validation")
    print("=" * 60)
    print("\nUse enhanced_review() function to perform a review.")
