"""
🎯 主控程序 - Agent编排器（Orchestrator）
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .arguments import get_config
from .tool import LLMClient, PromptBuilder, ContrastiveExampleManager, SelectedExamples
from .jsonchecker import JSONChecker, DISCREPANCY_SCHEMA, REFLECTION_SCHEMA

logger = logging.getLogger(__name__)


@dataclass
class PlannerResult:
    """Planner Agent 输出"""
    unfamiliar_terms: List[str] = field(default_factory=list)
    ambiguous_terms: List[str] = field(default_factory=list)
    key_risk_fields: List[str] = field(default_factory=list)
    raw_output: str = ""
    
    def is_empty(self) -> bool:
        return (len(self.unfamiliar_terms) == 0 and 
                len(self.ambiguous_terms) == 0 and 
                len(self.key_risk_fields) == 0)


@dataclass
class ReviewResult:
    """审核结果"""
    discrepancies: List[Dict[str, Any]] = field(default_factory=list)
    compliant_items: List[Dict[str, Any]] = field(default_factory=list)
    report: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class PlannerAgent:
    """规划 Agent - 识别专业术语和风险"""
    
    def __init__(self, llm_client: LLMClient, max_terms: int = 10):
        self.llm_client = llm_client
        self.max_terms = max_terms
        self.prompt_builder = PromptBuilder()
    
    def analyze(self, lc: Dict, invoice: Dict, bl: Dict, insurance: Dict) -> PlannerResult:
        """分析单据"""
        field_summary = self._build_summary(lc, invoice, bl, insurance)
        system_prompt, user_prompt = self.prompt_builder.get_planner_prompt(field_summary)
        
        try:
            answer = self.llm_client.call(system_prompt, user_prompt, temperature=0.2)
            result = self._parse_output(answer)
            result.raw_output = answer
            return result
        except Exception as e:
            logger.error(f"Planner failed: {e}")
            return PlannerResult(raw_output=str(e))
    
    def _build_summary(self, lc: Dict, invoice: Dict, bl: Dict, insurance: Dict) -> str:
        """构建字段摘要"""
        lines = ["=" * 60, "【单据字段摘要】", "=" * 60]
        
        lines.append("\n【信用证】")
        lines.append(f"货物描述: {lc.get('goods_description', '')}")
        lines.append(f"金额: {lc.get('amount', '')} {lc.get('currency', '')}")
        lines.append(f"贸易术语: {lc.get('trade_terms', '')}")
        
        lines.append("\n【商业发票】")
        lines.append(f"出具人: {invoice.get('issued_by', '')}")
        lines.append(f"金额: {invoice.get('total_amount', '')}")
        
        lines.append("\n【提单】")
        lines.append(f"托运人: {bl.get('shipper', '')}")
        lines.append(f"装货港: {bl.get('loading_port', '')}")
        lines.append(f"装船日期: {bl.get('shipped_on_board_date', '')}")
        
        lines.append("\n【保险单】")
        lines.append(f"险别: {insurance.get('coverage', '')}")
        
        return "\n".join(lines)
    
    def _parse_output(self, answer: str) -> PlannerResult:
        """解析输出"""
        import re
        result = PlannerResult()
        
        for keyword, target in [("陌生术语", "unfamiliar_terms"), 
                                 ("歧义表达", "ambiguous_terms"),
                                 ("关键风险", "key_risk_fields")]:
            pattern = rf"\*\*{keyword}\*\*[:：]\s*(.+?)(?=\n\*\*|$)"
            match = re.search(pattern, answer, re.IGNORECASE | re.DOTALL)
            if match:
                terms = [t.strip() for t in match.group(1).split("#") if t.strip()][:self.max_terms]
                setattr(result, target, terms)
        
        return result


class KnowledgeAgent:
    """知识增强 Agent"""
    
    def __init__(self, llm_client: LLMClient, embed_model, collection, top_k: int = 5):
        self.llm_client = llm_client
        self.embed_model = embed_model
        self.collection = collection
        self.top_k = top_k
        self.prompt_builder = PromptBuilder()
    
    def enhance(self, planner_result: PlannerResult) -> str:
        """知识增强"""
        if planner_result.is_empty():
            return ""
        
        term_knowledges = []
        for term in planner_result.unfamiliar_terms:
            knowledge = self._retrieve(term)
            if knowledge:
                term_knowledges.append((term, knowledge))
        
        return self._build_context(term_knowledges, planner_result.key_risk_fields)
    
    def _retrieve(self, term: str) -> str:
        """从 ChromaDB 检索"""
        try:
            query_embedding = self.embed_model.encode([term]).tolist()
            results = self.collection.query(query_embeddings=query_embedding, n_results=self.top_k)
            
            knowledges = []
            if results and 'documents' in results and results['documents']:
                for doc in results['documents'][0]:
                    if doc and doc not in knowledges:
                        knowledges.append(doc)
            
            return "\n\n".join(knowledges[:3])
        except Exception as e:
            logger.error(f"Retrieve failed: {e}")
            return ""
    
    def _build_context(self, term_knowledges: List, key_risk_fields: List[str]) -> str:
        """构建知识上下文"""
        lines = ["=" * 70, "【审核前知识增强】", "=" * 70]
        
        if term_knowledges:
            lines.append("\n📚 术语解释：")
            for i, (term, knowledge) in enumerate(term_knowledges, 1):
                lines.append(f"\n{i}. \"{term}\"")
                lines.append(f"   {knowledge[:500]}{'...' if len(knowledge) > 500 else ''}")
        
        if key_risk_fields:
            lines.append("\n\n⚠️ 重点风险提示：")
            for risk in key_risk_fields:
                lines.append(f"  • {risk}")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


class ReflectionAgent:
    """反思纠错 Agent"""
    
    def __init__(self, llm_client: LLMClient, max_loop: int = 5):
        self.llm_client = llm_client
        self.max_loop = max_loop
        self.prompt_builder = PromptBuilder()
    
    def reflect(self, discrepancies: List[Dict], lc: Dict, invoice: Dict, 
                bl: Dict, insurance: Dict, presentation_date: str = "") -> List[Dict]:
        """执行反思"""
        if not discrepancies:
            return []
        
        system_prompt, user_prompt = self.prompt_builder.get_reflection_prompt(
            discrepancies, lc, invoice, bl, insurance, presentation_date
        )
        
        try:
            result = self.llm_client.call_json(
                system_prompt, user_prompt, REFLECTION_SCHEMA, temperature=0.1, max_loop=self.max_loop
            )
            return self._apply(discrepancies, result)
        except Exception as e:
            logger.error(f"Reflection failed: {e}")
            return discrepancies
    
    def _apply(self, original: List[Dict], reflection_result: List[Dict]) -> List[Dict]:
        """应用反思结果"""
        result = []
        removed = set()
        modified = {}
        
        for r in reflection_result:
            action = r.get("action", "keep")
            idx = r.get("original_index")
            
            if action == "remove" and idx is not None:
                removed.add(idx)
            elif action == "modify" and idx is not None:
                item = original[idx].copy()
                for key in ["severity", "description", "ucp_reference", "field"]:
                    if key in r:
                        item[key] = r[key]
                modified[idx] = item
            elif action == "add":
                result.append({
                    "document": r.get("document", ""),
                    "field": r.get("field", ""),
                    "description": r.get("description", ""),
                    "ucp_reference": r.get("ucp_reference", ""),
                    "severity": r.get("severity", "一般"),
                    "reflection_note": "由反思 Agent 添加"
                })
        
        for i, item in enumerate(original):
            if i in removed:
                continue
            result.append(modified.get(i, item))
        
        return result


class ReviewOrchestrator:
    """审核编排器"""
    
    def __init__(self, config_path: str = "config/agent_config.json"):
        self.config = get_config(config_path)
        self.config.setup_logging()
        
        self.llm_client = LLMClient(self.config.llm)
        self.prompt_builder = PromptBuilder()
        
        self.planner = None
        self.knowledge = None
        self.reflection = None
        self.contrastive_manager = None
        
        self._init_agents()
    
    def _init_agents(self):
        """初始化 Agents"""
        if self.config.planner.enabled:
            self.planner = PlannerAgent(self.llm_client, self.config.planner.max_terms)
        
        if self.config.reflection.enabled:
            self.reflection = ReflectionAgent(self.llm_client, self.config.output_checker.max_loop)
        
        if self.config.contrastive.enabled:
            self.contrastive_manager = ContrastiveExampleManager(self.config.contrastive.data_dir)
    
    def review(self, lc_data: Dict, inv_data: Dict, bl_data: Dict, ins_data: Dict,
               presentation_date: str, embed_model=None, collection=None) -> ReviewResult:
        """执行完整审核"""
        logger.info("=" * 60)
        logger.info("Starting KDR-Agent V3 Review")
        logger.info("=" * 60)
        
        # Phase 1: Planner + Knowledge
        knowledge_context = ""
        planner_result = None
        
        if self.planner:
            try:
                planner_result = self.planner.analyze(lc_data, inv_data, bl_data, ins_data)
                if planner_result and not planner_result.is_empty() and embed_model and collection:
                    self.knowledge = KnowledgeAgent(
                        self.llm_client, embed_model, collection, self.config.knowledge.chromadb_top_k
                    )
                    knowledge_context = self.knowledge.enhance(planner_result)
            except Exception as e:
                logger.error(f"Phase 1 error: {e}")
        
        # Phase 2: 规则引擎
        rule_discrepancies, compliant_items = self._rule_check(
            lc_data, inv_data, bl_data, ins_data, presentation_date
        )
        
        # Phase 3: 增强版 AI
        ai_discrepancies = self._ai_review(
            lc_data, inv_data, bl_data, ins_data, presentation_date, knowledge_context
        )
        
        # Phase 4: 合并
        merged = self._merge(rule_discrepancies, ai_discrepancies)
        
        # Phase 5: 反思
        final = merged
        if self.reflection and merged:
            try:
                final = self.reflection.reflect(merged, lc_data, inv_data, bl_data, ins_data, presentation_date)
            except Exception as e:
                logger.error(f"Phase 5 error: {e}")
        
        logger.info(f"Review completed: {len(final)} discrepancies")
        
        return ReviewResult(
            discrepancies=final,
            compliant_items=compliant_items,
            metadata={
                "knowledge_enhanced": bool(knowledge_context),
                "contrastive_used": self.config.contrastive.enabled,
                "reflection_applied": self.config.reflection.enabled and bool(merged),
                "version": "v3_kdr_agent"
            }
        )
    
    def _rule_check(self, lc: Dict, inv: Dict, bl: Dict, ins: Dict, presentation_date: str):
        """规则引擎检查"""
        try:
            from check_v2 import check_calculations
            return check_calculations(lc, inv, bl, ins, presentation_date)
        except Exception as e:
            logger.error(f"Rule check failed: {e}")
            return [], []
    
    def _ai_review(self, lc: Dict, inv: Dict, bl: Dict, ins: Dict,
                   presentation_date: str, knowledge_context: str) -> List[Dict]:
        """AI 审核"""
        contrastive_text = ""
        if self.contrastive_manager:
            try:
                selected = self.contrastive_manager.select_relevant(lc, inv, bl, ins)
                contrastive_text = self.contrastive_manager.format_for_prompt(
                    selected, self.config.contrastive.max_positive,
                    self.config.contrastive.max_negative, self.config.contrastive.max_boundary
                )
            except Exception as e:
                logger.error(f"Contrastive failed: {e}")
        
        system_prompt = self.prompt_builder.get_contrastive_system_prompt(contrastive_text, knowledge_context)
        user_prompt = self.prompt_builder.get_contrastive_user_prompt(lc, inv, bl, ins, presentation_date)
        
        try:
            result = self.llm_client.call_json(
                system_prompt, user_prompt, DISCREPANCY_SCHEMA,
                temperature=0.2, max_loop=self.config.output_checker.max_loop
            )
            return result if isinstance(result, list) else [result] if result else []
        except Exception as e:
            logger.error(f"AI review failed: {e}")
            return []
    
    def _merge(self, rule_disc: List[Dict], ai_disc: List[Dict]) -> List[Dict]:
        """合并去重"""
        try:
            from check_v2 import merge_discrepancies
            return merge_discrepancies(rule_disc, ai_disc)
        except Exception:
            seen = set()
            merged = []
            for d in rule_disc + ai_disc:
                key = (d.get("document"), d.get("field"), d.get("description"))
                if key not in seen:
                    seen.add(key)
                    merged.append(d)
            return merged


def review_documents(lc_data: Dict, inv_data: Dict, bl_data: Dict, ins_data: Dict,
                    presentation_date: str, config_path: str = "config/agent_config.json",
                    embed_model=None, collection=None) -> ReviewResult:
    """便捷函数"""
    orchestrator = ReviewOrchestrator(config_path)
    return orchestrator.review(lc_data, inv_data, bl_data, ins_data, presentation_date, embed_model, collection)


if __name__ == "__main__":
    print("=" * 70)
    print("KDR-Agent V3 信用证审核系统")
    print("=" * 70)
