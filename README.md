# The-LC-Checker 核心实现

V2 RAG 检索增强 + V3 多 Agent 协同的最小化核心代码。

## 文件结构

```
.
├── v2rag_core/
│   └── rag_retriever.py      # V2: RAG 检索增强 (3.5KB)
└── v3agent_core/
    └── agents.py             # V3: 多 Agent 协同 (10.6KB)
```

## V2 RAG 检索增强

**文件**: `v2rag_core/rag_retriever.py`

**核心功能**:
- `RAGRetriever` - 基于 Embedding + ChromaDB 的知识检索
- `get_ucp_knowledge()` - 获取 UCP600 相关条款

**使用方法**:
```python
from v2rag_core.rag_retriever import RAGRetriever, get_ucp_knowledge

# 方式1: 使用类
retriever = RAGRetriever()
docs = retriever.retrieve("保险险别要求", top_k=3)

# 方式2: 便捷函数
knowledge = get_ucp_knowledge("信用证金额容差")
```

## V3 多 Agent 协同

**文件**: `v3agent_core/agents.py`

**核心组件**:
1. `PlannerAgent` - 识别专业术语和风险字段
2. `KnowledgeAgent` - RAG 知识增强
3. `ReflectionAgent` - 审核结果复核
4. `MultiAgentOrchestrator` - 编排器，协调三 Agent

**使用方法**:
```python
from v3agent_core.agents import multi_agent_review
from v2rag_core.rag_retriever import RAGRetriever

# 准备数据
lc = {"amount": 100000, "currency": "USD", "goods_description": "..."}
inv = {"total_amount": 100000, "currency": "USD"}
bl = {"shipper": "Seller Co.", "shipped_on_board_date": "2024-03-01"}
ins = {"coverage": "All Risks"}

# 创建检索器
retriever = RAGRetriever()

# 执行多 Agent 审核
result = multi_agent_review(
    lc, inv, bl, ins, 
    presentation_date="2024-03-10",
    retrieve_func=lambda q: retriever.retrieve(q, top_k=3)
)

# 查看结果
print(f"发现 {len(result.discrepancies)} 个不符点")
print(result.knowledge_context)
```

## 依赖

```bash
pip install openai chromadb sentence-transformers
```

## 架构说明

```
用户输入
    ↓
[PlannerAgent] 识别术语 → [KnowledgeAgent] 检索知识
    ↓
[AI Review] 基于知识审核
    ↓
[ReflectionAgent] 复核结果
    ↓
输出不符点
```
