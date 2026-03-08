# v3agent V3

基于多智能体架构的信用证单据审核系统。

## 架构（V3-Agent 标准）

```
v3agent/
├── main.py              # 🎯 主控程序 - Agent编排器（Orchestrator）
├── tool.py              # 🛠️ 工具模块 - Prompt生成 & API封装
├── arguments.py         # ⚙️ 配置管理 - 参数加载
├── jsonchecker.py       # ✅ 验证模块 - JSON结构校验
├── requirements.txt     # 📦 依赖清单
└── __init__.py          # 包入口
```

## 快速开始

```python
from v3agent import review_documents

# 执行审核
result = review_documents(
    lc_data=letter_of_credit_dict,
    inv_data=invoice_dict,
    bl_data=bill_of_lading_dict,
    ins_data=insurance_dict,
    presentation_date="2024-03-01"
)

# 查看结果
print(f"发现 {len(result.discrepancies)} 个不符点")
for d in result.discrepancies:
    print(f"- [{d['severity']}] {d['document']}/{d['field']}: {d['description']}")
```

## 配置

配置文件路径：`config/agent_config.json`

```json
{
  "agents": {
    "planner": {"enabled": true, "max_terms": 10},
    "knowledge": {"enabled": true, "chromadb_top_k": 5},
    "reflection": {"enabled": true}
  },
  "llm": {
    "model_name": "qwen2.5:14b",
    "base_url_env": "OPENAI_API_BASE",
    "api_key_env": "OPENAI_API_KEY"
  }
}
```

## Agents 说明

| Agent | 职责 |
|-------|------|
| **Planner** | 识别单据中的专业术语和风险字段 |
| **Knowledge** | 通过 RAG 检索 UCP600 知识，增强理解 |
| **Reflection** | 复核审核结果，修正误报和漏报 |

## 审核流程

```
Phase 1: Planner → Knowledge (术语识别 & 知识增强)
    ↓
Phase 2: 规则引擎 (复用 check_v2)
    ↓
Phase 3: 增强版 AI 审核 (注入知识 + 对比样本)
    ↓
Phase 4: 合并去重
    ↓
Phase 5: Reflection (反思纠错)
    ↓
Phase 6: 输出结果
```

## 与原 agent_enhance 的关系

本模块完全替代了原有的 `agent_enhance/` 目录和 `enhanced_review.py` 文件，按照 V3-Agent 标准架构重新组织代码：

| 原文件 | 新位置 |
|--------|--------|
| `agent_enhance/planner_agent.py` | `main.py` - `PlannerAgent` |
| `agent_enhance/knowledge_agent.py` | `main.py` - `KnowledgeAgent` |
| `agent_enhance/reflection_agent.py` | `main.py` - `ReflectionAgent` |
| `agent_enhance/llm_client.py` | `tool.py` - `LLMClient` |
| `agent_enhance/output_checker.py` | `jsonchecker.py` - `JSONChecker` |
| `agent_enhance/contrastive_examples.py` | `tool.py` - `ContrastiveExampleManager` |
| `agent_enhance/prompts/*.py` | `tool.py` - `PromptBuilder` |
| `enhanced_review.py` | `main.py` - `ReviewOrchestrator` |
