"""
知识增强 Agent (Knowledge Agent)

对 Planner 识别出的陌生术语和歧义表达，分别通过 ChromaDB 知识库检索
和 LLM 上下文消歧获取准确解释，汇总为一段"背景知识摘要"。
"""

import logging
from typing import Dict, List, Any, Optional, Tuple

from agent_enhance.llm_client import AgentLLMClient
from agent_enhance.planner_agent import PlannerResult
from agent_enhance.prompts.knowledge_prompt import get_knowledge_prompt
from agent_enhance.prompts.disambiguation_prompt import get_disambiguation_prompt

logger = logging.getLogger(__name__)


class KnowledgeAgent:
    """
    知识增强 Agent
    
    职责：
    1. 从 ChromaDB 检索术语对应的 UCP600 条款
    2. 调用 LLM 对歧义表达做上下文消歧
    3. 构建格式化的知识上下文
    """
    
    def __init__(
        self,
        llm_client: AgentLLMClient,
        embed_model,
        collection,
        top_k: int = 5
    ):
        """
        初始化 Knowledge Agent
        
        Args:
            llm_client: LLM 客户端
            embed_model: 嵌入模型（复用 check_v2 的 embed_model）
            collection: ChromaDB 集合（复用 check_v2 的 collection）
            top_k: 检索返回的最大结果数
        """
        self.llm_client = llm_client
        self.embed_model = embed_model
        self.collection = collection
        self.top_k = top_k
    
    def enhance(
        self,
        planner_result: PlannerResult,
        doc_context: str = ""
    ) -> str:
        """
        完整知识增强流程
        
        Args:
            planner_result: Planner Agent 的分析结果
            doc_context: 文档上下文（可选）
            
        Returns:
            格式化的知识上下文字符串
        """
        if planner_result.is_empty():
            logger.info("Planner result is empty, skipping knowledge enhancement")
            return ""
        
        # 1. 检索术语知识
        term_knowledges = []
        for term in planner_result.unfamiliar_terms:
            knowledge = self._retrieve_term_knowledge(term)
            if knowledge:
                term_knowledges.append((term, knowledge))
        
        # 2. 消歧处理
        disambiguation = ""
        if planner_result.ambiguous_terms:
            disambiguation = self._disambiguate_terms(
                planner_result.ambiguous_terms,
                doc_context
            )
        
        # 3. 构建知识上下文
        knowledge_context = self._build_knowledge_context(
            term_knowledges,
            disambiguation,
            planner_result.key_risk_fields
        )
        
        logger.info(f"Knowledge enhancement complete: {len(term_knowledges)} terms, "
                   f"{len(planner_result.ambiguous_terms)} ambiguous terms")
        
        return knowledge_context
    
    def _retrieve_term_knowledge(self, term: str) -> str:
        """
        从 ChromaDB 检索术语对应的 UCP600 条款
        
        Args:
            term: 待检索的术语
            
        Returns:
            检索到的知识文本
        """
        try:
            # 使用嵌入模型编码查询
            query_embedding = self.embed_model.encode([term]).tolist()
            
            # 查询 ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=self.top_k
            )
            
            # 整合结果
            knowledges = []
            if results and 'documents' in results and results['documents']:
                for doc in results['documents'][0]:
                    if doc and doc not in knowledges:
                        knowledges.append(doc)
            
            # 截取前3个结果
            knowledge_text = "\n\n".join(knowledges[:3])
            
            if knowledge_text:
                logger.debug(f"Retrieved knowledge for term '{term}': {len(knowledge_text)} chars")
            
            return knowledge_text
            
        except Exception as e:
            logger.error(f"Failed to retrieve knowledge for term '{term}': {e}")
            return ""
    
    def _disambiguate_terms(
        self,
        terms: List[str],
        doc_context: str
    ) -> str:
        """
        调用 LLM 对歧义表达做上下文消歧
        
        Args:
            terms: 歧义表达列表
            doc_context: 文档上下文
            
        Returns:
            消歧结果文本
        """
        if not terms:
            return ""
        
        system_prompt, user_prompt = get_disambiguation_prompt(terms, doc_context)
        
        try:
            answer = self.llm_client.call(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1  # 低温度，更确定
            )
            
            logger.debug(f"Disambiguation result: {len(answer)} chars")
            return answer
            
        except Exception as e:
            logger.error(f"Disambiguation failed: {e}")
            return ""
    
    def _build_knowledge_context(
        self,
        term_knowledges: List[Tuple[str, str]],
        disambiguation: str,
        key_risk_fields: List[str]
    ) -> str:
        """
        将所有知识拼接成最终的上下文字符串
        
        Args:
            term_knowledges: 术语知识列表 [(term, knowledge), ...]
            disambiguation: 消歧结果
            key_risk_fields: 关键风险字段
            
        Returns:
            格式化的知识上下文
        """
        lines = []
        lines.append("=" * 70)
        lines.append("【审核前知识增强 —— 由 Knowledge Agent 提供】")
        lines.append("=" * 70)
        
        # 术语解释
        if term_knowledges:
            lines.append("\n📚 术语解释：")
            lines.append("-" * 40)
            for i, (term, knowledge) in enumerate(term_knowledges, 1):
                lines.append(f"\n{i}. \"{term}\"")
                # 截断过长的知识
                if len(knowledge) > 500:
                    knowledge = knowledge[:500] + "..."
                lines.append(f"   {knowledge}")
        
        # 上下文消歧
        if disambiguation:
            lines.append("\n\n🔍 上下文消歧：")
            lines.append("-" * 40)
            lines.append(disambiguation)
        
        # 重点风险提示
        if key_risk_fields:
            lines.append("\n\n⚠️ 重点风险提示：")
            lines.append("-" * 40)
            for risk in key_risk_fields:
                lines.append(f"  • {risk}")
        
        lines.append("\n" + "=" * 70)
        
        return "\n".join(lines)
    
    def quick_enhance(self, terms: List[str]) -> Dict[str, str]:
        """
        快速增强：仅检索术语知识，不调用 LLM 消歧
        
        Args:
            terms: 术语列表
            
        Returns:
            术语 -> 知识的字典
        """
        result = {}
        for term in terms:
            knowledge = self._retrieve_term_knowledge(term)
            if knowledge:
                result[term] = knowledge
        return result
