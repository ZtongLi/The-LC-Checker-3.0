"""
V2 RAG 检索增强 - 核心实现
功能：基于 Embedding + ChromaDB 的 UCP600 条款检索
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Optional


class RAGRetriever:
    """
    RAG 检索器 - 用于检索相关 UCP600 条款
    """
    
    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5", 
                 db_path: str = "./chroma_db"):
        self.model_name = model_name
        self.db_path = db_path
        self._embed_model: Optional[SentenceTransformer] = None
        self._collection = None
        self._chroma_client = None
    
    def _get_embed_model(self) -> SentenceTransformer:
        """延迟加载 Embedding 模型"""
        if self._embed_model is None:
            print(f"🔄 加载 Embedding 模型: {self.model_name}")
            os.environ["HF_HUB_OFFLINE"] = "1"
            self._embed_model = SentenceTransformer(self.model_name)
        return self._embed_model
    
    def _get_collection(self):
        """获取 ChromaDB 集合"""
        if self._collection is None:
            self._chroma_client = chromadb.PersistentClient(path=self.db_path)
            self._collection = self._chroma_client.get_or_create_collection(
                name="ucp600", 
                metadata={"hnsw:space": "cosine"}
            )
        return self._collection
    
    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        检索与查询相关的 UCP600 条款
        
        Args:
            query: 查询文本（如 "保险险别要求"）
            top_k: 返回结果数量
            
        Returns:
            相关条款文本列表
        """
        try:
            # 编码查询
            embed_model = self._get_embed_model()
            query_embedding = embed_model.encode([query]).tolist()
            
            # 检索
            collection = self._get_collection()
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=top_k
            )
            
            # 提取文档
            documents = []
            if results and 'documents' in results and results['documents']:
                for doc in results['documents'][0]:
                    if doc:
                        documents.append(doc)
            
            return documents
            
        except Exception as e:
            print(f"❌ 检索失败: {e}")
            return []


# 便捷函数
def get_ucp_knowledge(query: str, top_k: int = 3) -> str:
    """
    获取与查询相关的 UCP600 知识
    
    Args:
        query: 查询文本
        top_k: 返回结果数量
        
    Returns:
        格式化的知识文本
    """
    retriever = RAGRetriever()
    docs = retriever.retrieve(query, top_k)
    
    if not docs:
        return ""
    
    return "\n\n".join([f"[知识 {i+1}]\n{doc}" for i, doc in enumerate(docs)])


if __name__ == "__main__":
    # 测试
    print("=" * 60)
    print("V2 RAG 检索测试")
    print("=" * 60)
    
    retriever = RAGRetriever()
    
    test_queries = [
        "保险单必须覆盖哪些险别",
        "信用证金额容差规定",
        "提单清洁要求"
    ]
    
    for query in test_queries:
        print(f"\n🔍 查询: {query}")
        results = retriever.retrieve(query, top_k=2)
        for i, doc in enumerate(results, 1):
            print(f"  结果 {i}: {doc[:100]}...")
