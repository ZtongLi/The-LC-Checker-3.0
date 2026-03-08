"""
V3 多 Agent 协同 - 核心实现
功能：Planner + Knowledge + Reflection 三 Agent 协同审核
"""

import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


# ==================== 数据类 ====================

@dataclass
class PlannerResult:
    """Planner Agent 输出"""
    unfamiliar_terms: List[str] = field(default_factory=list)
    ambiguous_terms: List[str] = field(default_factory=list)
    key_risk_fields: List[str] = field(default_factory=list)


@dataclass
class ReviewResult:
    """审核结果"""
    discrepancies: List[Dict[str, Any]] = field(default_factory=list)
    knowledge_context: str = ""


# ==================== LLM 客户端 ====================

class SimpleLLMClient:
    """简化版 LLM 客户端"""
    
    def __init__(self, model: str = "qwen2.5:14b", 
                 base_url: str = "http://localhost:11434/v1"):
        self.model = model
        self.base_url = base_url
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(
                base_url=self.base_url,
                api_key="ollama"
            )
        return self._client
    
    def call(self, system: str, user: str, temperature: float = 0.1) -> str:
        """调用 LLM"""
        try:
            client = self._get_client()
            resp = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                temperature=temperature
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ LLM 调用失败: {e}")
            return ""


# ==================== Agent 1: Planner ====================

class PlannerAgent:
    """
    规划 Agent - 识别单据中的专业术语和风险
    """
    
    def __init__(self, llm: SimpleLLMClient):
        self.llm = llm
    
    def analyze(self, lc: Dict, invoice: Dict, bl: Dict, insurance: Dict) -> PlannerResult:
        """分析单据，识别术语"""
        
        system = """你是信用证审核专家。请分析单据，识别：
1. 陌生术语（如保险险别、贸易术语）
2. 歧义表达（如约数词）
3. 关键风险字段（金额容差、日期等）

输出格式：
陌生术语: term1#term2
歧义表达: term3#term4
关键风险: field1#field2"""

        user = f"""信用证：{lc.get('goods_description', '')} {lc.get('amount', '')}
发票：{invoice.get('issued_by', '')} {invoice.get('total_amount', '')}
提单：{bl.get('shipper', '')} {bl.get('loading_port', '')}
保险单：{insurance.get('coverage', '')}"""

        response = self.llm.call(system, user, temperature=0.2)
        return self._parse(response)
    
    def _parse(self, text: str) -> PlannerResult:
        """解析输出"""
        import re
        result = PlannerResult()
        
        for keyword, attr in [("陌生术语", "unfamiliar_terms"), 
                               ("歧义表达", "ambiguous_terms"),
                               ("关键风险", "key_risk_fields")]:
            match = re.search(rf"{keyword}[:：]\s*(.+?)(?=\n|$)", text)
            if match:
                terms = [t.strip() for t in match.group(1).split("#") if t.strip()]
                setattr(result, attr, terms)
        
        return result


# ==================== Agent 2: Knowledge ====================

class KnowledgeAgent:
    """
    知识增强 Agent - RAG 检索 UCP600 知识
    """
    
    def __init__(self, llm: SimpleLLMClient):
        self.llm = llm
    
    def enhance(self, planner_result: PlannerResult, 
                retrieve_func=None) -> str:
        """
        知识增强
        
        Args:
            planner_result: Planner 分析结果
            retrieve_func: 外部检索函数，接收 query 返回知识列表
        """
        if planner_result.is_empty():
            return ""
        
        contexts = []
        
        # 检索陌生术语
        for term in planner_result.unfamiliar_terms:
            if retrieve_func:
                docs = retrieve_func(term)
                if docs:
                    contexts.append(f"📚 {term}:\n" + "\n".join(docs[:2]))
        
        if not contexts:
            return ""
        
        return "【知识增强】\n" + "\n\n".join(contexts)


# ==================== Agent 3: Reflection ====================

class ReflectionAgent:
    """
    反思 Agent - 复核审核结果
    """
    
    def __init__(self, llm: SimpleLLMClient):
        self.llm = llm
    
    def reflect(self, discrepancies: List[Dict], 
                lc: Dict, invoice: Dict, bl: Dict, insurance: Dict) -> List[Dict]:
        """反思复核"""
        
        if not discrepancies:
            return []
        
        system = """你是资深审核专家。请复核以下不符点，判断：
1. 是否真实存在
2. UCP 条款引用是否正确
3. 严重程度是否合理
4. 是否有遗漏

对每项输出：保留/删除/修改/新增"""

        user = "不符点列表：\n"
        for i, d in enumerate(discrepancies):
            user += f"{i}. [{d.get('severity')}] {d.get('document')}/{d.get('field')}: {d.get('description')}\n"
        
        response = self.llm.call(system, user, temperature=0.1)
        
        # 简化处理：根据关键词过滤
        result = []
        for d in discrepancies:
            desc = d.get('description', '')
            # 简单规则：保留所有（实际应根据 LLM 输出精细处理）
            result.append(d)
        
        return result


# ==================== 编排器 ====================

class MultiAgentOrchestrator:
    """
    多 Agent 编排器 - 协调三 Agent 工作
    """
    
    def __init__(self, retrieve_func=None):
        """
        Args:
            retrieve_func: 外部 RAG 检索函数
        """
        self.llm = SimpleLLMClient()
        self.planner = PlannerAgent(self.llm)
        self.knowledge = KnowledgeAgent(self.llm)
        self.reflection = ReflectionAgent(self.llm)
        self.retrieve_func = retrieve_func
    
    def review(self, lc: Dict, invoice: Dict, bl: Dict, 
               insurance: Dict, presentation_date: str) -> ReviewResult:
        """
        执行多 Agent 协同审核
        
        Returns:
            ReviewResult 包含不符点和知识上下文
        """
        print("🚀 多 Agent 协同审核开始...")
        
        # Step 1: Planner 分析
        print("  [Planner] 识别术语和风险...")
        planner_result = self.planner.analyze(lc, invoice, bl, insurance)
        print(f"      发现 {len(planner_result.unfamiliar_terms)} 个陌生术语")
        
        # Step 2: Knowledge 增强
        print("  [Knowledge] 检索相关知识...")
        knowledge_context = self.knowledge.enhance(planner_result, self.retrieve_func)
        if knowledge_context:
            print(f"      获取到知识增强")
        
        # Step 3: AI 审核（简化版，实际应调用 LLM）
        print("  [AI Review] 基于知识审核单据...")
        discrepancies = self._ai_review(lc, invoice, bl, insurance, knowledge_context)
        print(f"      发现 {len(discrepancies)} 个潜在不符点")
        
        # Step 4: Reflection 复核
        if discrepancies:
            print("  [Reflection] 复核审核结果...")
            discrepancies = self.reflection.reflect(discrepancies, lc, invoice, bl, insurance)
            print(f"      复核后剩余 {len(discrepancies)} 个不符点")
        
        print("✅ 多 Agent 协同审核完成")
        
        return ReviewResult(
            discrepancies=discrepancies,
            knowledge_context=knowledge_context
        )
    
    def _ai_review(self, lc: Dict, invoice: Dict, bl: Dict, 
                   insurance: Dict, knowledge: str) -> List[Dict]:
        """AI 审核 - 简化版"""
        
        system = f"""你是信用证审核专家。{knowledge}

请审核单据，输出 JSON 格式不符点：
[{{"document": "单据名", "field": "字段", "description": "描述", 
   "ucp_reference": "UCP条款", "severity": "严重/一般/轻微"}}]

无不符点时返回 []。"""

        user = f"""信用证金额: {lc.get('amount')} {lc.get('currency')}
发票金额: {invoice.get('total_amount')} {invoice.get('currency')}
提单日期: {bl.get('shipped_on_board_date')}
保险险别: {insurance.get('coverage')}"""

        response = self.llm.call(system, user, temperature=0.2)
        
        # 简化：尝试解析 JSON，失败返回空列表
        try:
            import json
            # 提取 JSON 部分
            import re
            match = re.search(r'\[.*?\]', response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except:
            pass
        
        return []


# ==================== 便捷函数 ====================

def multi_agent_review(lc_data: Dict, inv_data: Dict, bl_data: Dict, 
                       ins_data: Dict, presentation_date: str,
                       retrieve_func=None) -> ReviewResult:
    """
    便捷函数：执行多 Agent 审核
    
    Args:
        lc_data: 信用证数据
        inv_data: 发票数据
        bl_data: 提单数据
        ins_data: 保险单数据
        presentation_date: 交单日期
        retrieve_func: 可选的 RAG 检索函数
        
    Returns:
        ReviewResult 审核结果
    """
    orchestrator = MultiAgentOrchestrator(retrieve_func)
    return orchestrator.review(lc_data, inv_data, bl_data, ins_data, presentation_date)


if __name__ == "__main__":
    print("=" * 60)
    print("V3 多 Agent 协同 - 核心实现")
    print("=" * 60)
    
    # 模拟测试数据
    lc = {"amount": 100000, "currency": "USD", "goods_description": "Electronic Products"}
    inv = {"total_amount": 100000, "currency": "USD", "issued_by": "Seller Co."}
    bl = {"shipper": "Seller Co.", "loading_port": "Shanghai", "shipped_on_board_date": "2024-03-01"}
    ins = {"coverage": "All Risks", "sum_insured": "110000 USD"}
    
    # 模拟检索函数
    def mock_retrieve(query: str) -> List[str]:
        return [f"关于 {query} 的 UCP600 条款说明..."]
    
    # 执行审核
    result = multi_agent_review(lc, inv, bl, ins, "2024-03-10", mock_retrieve)
    
    print(f"\n最终不符点数量: {len(result.discrepancies)}")
