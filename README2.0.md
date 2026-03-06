# 信用证智能审单系统 V3.0

[![Docker](https://img.shields.io/badge/Docker-Supported-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-orange)](https://fastapi.tiangolo.com/)
[![Version](https://img.shields.io/badge/Version-3.0-purple)](https://github.com/)

> 基于 **Multi-Agent + RAG + 对比学习** 的下一代信用证审单系统

---

## 🆕 V3.0 重大更新

本次更新引入了 **KDR-Agent** 架构，通过多智能体协作、知识增强和对比学习，大幅提升审单准确率和专业深度。

### 核心升级对比

| 维度 | V2.0 | V3.0 (本次更新) |
|------|------|-----------------|
| **架构** | 单路 AI 审核 | 多智能体协作 (Multi-Agent) |
| **知识利用** | 基础 RAG 检索 | 知识增强预理解 (Knowledge Agent) |
| **输出质量** | 直接输出 | 反思纠错 (Reflection Agent) |
| **学习方式** | 静态提示词 | 对比学习示例 (Contrastive Learning) |
| **校验机制** | 简单校验 | JSON Schema + 自动修复 |
| **配置方式** | 硬编码 | 灵活 JSON 配置 |

---

## 🏗️ V3.0 架构详解

### 多智能体协作流程 (Phase 0-6)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         LC Checker V3.0 架构                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Phase 0        Phase 1         Phase 2        Phase 3                  │
│  ┌─────┐      ┌─────────┐     ┌─────────┐   ┌─────────────────┐        │
│  │ OCR │  →   │ PLANNER │  →  │ 规则引擎 │ → │ 增强版 AI 审核   │        │
│  │提取 │      │  Agent  │     │(check_v2)│   │                 │        │
│  └─────┘      └────┬────┘     └─────────┘   └─────────────────┘        │
│                    │                                                    │
│                    ↓                                                    │
│              ┌───────────┐                                             │
│              │ KNOWLEDGE │  ← ChromaDB (UCP600 知识库)                  │
│              │  Agent    │                                             │
│              └─────┬─────┘                                             │
│                    │                                                    │
│                    ↓ 知识上下文                                         │
│  Phase 4        Phase 5        Phase 6                                  │
│  ┌─────────┐   ┌───────────┐  ┌───────────────┐                        │
│  │合并去重 │ → │REFLECTION │ → │  生成报告     │                        │
│  │         │   │  Agent    │   │               │                        │
│  └─────────┘   └───────────┘   └───────────────┘                        │
│                    ↑                                                    │
│              对比学习示例 (Positive/Negative/Boundary)                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 智能体职责说明

| 智能体 | 职责 | 核心技术 |
|--------|------|----------|
| **Planner Agent** | 预扫描单据，识别专业术语和歧义表达 | 字段分析 + LLM 判断 |
| **Knowledge Agent** | 检索 UCP600 条款，消歧术语 | RAG + 上下文消歧 |
| **Reflection Agent** | 复核输出质量，纠错优化 | 4 维度检查标准 |
| **Output Checker** | 结构化输出校验与修复 | JSON Schema + 重试机制 |

---

## 📦 新增模块

### 1. Agent 增强模块 (`agent_enhance/`)

```
agent_enhance/
├── __init__.py                 # 模块入口，统一暴露接口
├── planner_agent.py            # 规划智能体 - 术语识别与风险标记
├── knowledge_agent.py          # 知识智能体 - UCP600 条款检索与消歧
├── reflection_agent.py         # 反思智能体 - 4 维度质量检查
├── output_checker.py           # 输出校验器 - JSON Schema 校验
├── llm_client.py               # LLM 客户端封装
├── contrastive_examples.py     # 对比学习示例管理
└── prompts/                    # 提示词模板库
    ├── __init__.py
    ├── planner_prompt.py       # Planner 提示词
    ├── knowledge_prompt.py     # Knowledge 提示词
    ├── disambiguation_prompt.py # 消歧提示词
    ├── reflection_prompt.py    # Reflection 提示词
    └── contrastive_prompt.py   # 对比学习提示词
```

### 2. 对比学习数据集 (`contrastive_data/`)

包含 700+ 条专业标注示例，用于提升 AI 审核的边界判断能力：

| 数据类型 | 数量 | 说明 |
|----------|------|------|
| `positive_cases.json` | 361 条 | 正确审核示例（符合 UCP600）|
| `negative_cases.json` | 259 条 | 错误审核示例（常见错误模式）|
| `boundary_cases.json` | 117 条 | 边界案例（模糊地带的处理）|

### 3. 增强审核编排器 (`enhanced_review.py`)

V3.0 的统一入口，编排 Phase 0-6 的完整流程：

```python
from enhanced_review import enhanced_review

result = enhanced_review(
    lc_data=lc_structured,      # 信用证结构化数据
    inv_data=inv_structured,    # 发票结构化数据
    bl_data=bl_structured,      # 提单结构化数据
    ins_data=ins_structured,    # 保险单结构化数据
    presentation_date="2024-03-15",
    config_path="config/agent_config.json"
)
```

### 4. 配置文件 (`config/agent_config.json`)

灵活配置各模块参数：

```json
{
  "version": "3.0",
  "agents": {
    "planner": {"enabled": true, "max_terms": 10, "temperature": 0.2},
    "knowledge": {"enabled": true, "chromadb_top_k": 5, "temperature": 0.1},
    "reflection": {"enabled": true, "temperature": 0.1}
  },
  "contrastive_examples": {
    "enabled": true,
    "max_positive": 5,
    "max_negative": 5,
    "max_boundary": 3
  },
  "fallback": {
    "on_planner_fail": "skip",
    "on_knowledge_fail": "skip",
    "on_reflection_fail": "use_original",
    "on_all_fail": "fallback_to_v2"
  }
}
```

### 5. 测试工具集

| 工具 | 功能 |
|------|------|
| `test_recall.py` | 知识库召回率测试（RAG 性能评估）|
| `test_v2_vs_v3.py` | V2 与 V3 审核结果对比测试 |

---

## 🎯 V3.0 核心特性

### 1. 知识增强预理解

在正式审核前，Planner Agent 会：
- 扫描 4 份单据的所有字段
- 识别专业术语（如贸易术语、保险险别等）
- 标记歧义表达（如 "approximately", "about" 等）
- 检索 UCP600 相关条款作为背景知识

### 2. 4 维度反思纠错

Reflection Agent 按以下标准复核每个不符点：

| 维度 | 检查内容 |
|------|----------|
| **字段准确性** | 不符点涉及的字段值是否真实存在差异 |
| **UCP 条款正确性** | 引用的 UCP600 条款是否适用 |
| **严重程度合理性** | 严重/一般/轻微的判定是否合理 |
| **遗漏检查** | 是否有应检未检的不符点 |

### 3. 对比学习增强

在审核提示词中动态注入：
- ✅ 正面示例：正确的审核方式
- ❌ 负面示例：常见错误模式
- ⚠️ 边界示例：模糊地带的处理

### 4. 容错与降级

当任一 Agent 失败时，系统会：
1. 按配置执行降级策略（跳过/使用原始值/回退到 V2）
2. 记录失败日志
3. 保证审核流程不中断

---

## 🚀 快速开始

### 环境要求

与 V2.0 相同，无需额外依赖：
- Docker 20.10+
- Docker Compose 2.0+

### 启动方式

**方式一：使用一键恢复脚本**

```bash
curl -fsSL https://raw.githubusercontent.com/ZtongLi/The-LC-Checker/main/restore.sh | bash
```

**方式二：手动启动**

```bash
# 1. 克隆代码
git clone https://github.com/ZtongLi/The-LC-Checker-2.0-vision.git
cd lc-checker

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填写 OpenAI API Key

# 3. 启动服务
docker-compose up -d

# 4. 访问服务
# 前端页面: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### V3.0 配置

编辑 `config/agent_config.json` 可调整：
- 各 Agent 的开关和参数
- LLM 模型选择（默认使用 qwen2.5:14b）
- 降级策略
- 日志级别

---

## 📊 项目结构

```
lc-checker/
├── app/                          # 前端 React 项目
├── server.py                     # FastAPI 后端服务
├── check_v2.py                   # V2 审核核心（复用）
├── ocr_extract.py                # OCR 文字提取（复用）
├── build_knowledge_base.py       # 知识库构建（复用）
│
├── 🆕 enhanced_review.py         # V3 增强版审核入口
├── 🆕 agent_enhance/             # 多智能体增强模块
│   ├── planner_agent.py
│   ├── knowledge_agent.py
│   ├── reflection_agent.py
│   ├── output_checker.py
│   ├── llm_client.py
│   ├── contrastive_examples.py
│   └── prompts/
│
├── 🆕 config/
│   └── agent_config.json         # V3 配置文件
│
├── 🆕 contrastive_data/          # 对比学习数据集
│   ├── positive_cases.json
│   ├── negative_cases.json
│   └── boundary_cases.json
│
├── 🆕 test_recall.py             # 召回率测试
├── 🆕 test_v2_vs_v3.py           # 版本对比测试
│
├── knowledge_base/               # UCP600 知识库原文
├── chroma_db/                    # 向量数据库
├── test_data/                    # 测试数据集
├── test_pdf/                     # 测试 PDF 样本
├── Dockerfile                    # Docker 构建配置
├── docker-compose.yml            # Docker Compose 配置
├── restore.sh                    # 一键恢复脚本
├── requirements.txt              # Python 依赖
├── README.md                     # V2 版本文档
└── README2.0.md                  # V3 版本文档（本文件）
```

---

## 🧪 测试与评估

### 1. 知识库召回率测试

```bash
# 测试 RAG 检索效果
python test_recall.py
```

### 2. V2 vs V3 对比测试

```bash
# 对比两个版本的审核结果
python test_v2_vs_v3.py
```

### 3. 单样本测试

```bash
# 使用测试用例进行验证
python test_full_pipeline.py
```

---

## ⚙️ 配置说明

### 环境变量 (.env)

```bash
# OpenAI API 配置（V3 默认使用本地 Ollama，可修改配置使用其他模型）
OPENAI_API_KEY=ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL=qwen2.5:14b
```

### Agent 配置 (config/agent_config.json)

```json
{
  "agents": {
    "planner": {
      "enabled": true,        // 是否启用 Planner Agent
      "max_terms": 10,        // 最大识别术语数
      "temperature": 0.2      // LLM 温度参数
    },
    "knowledge": {
      "enabled": true,        // 是否启用 Knowledge Agent
      "chromadb_top_k": 5,    // RAG 检索条数
      "temperature": 0.1
    },
    "reflection": {
      "enabled": true,        // 是否启用 Reflection Agent
      "temperature": 0.1,
      "dimensions": [         // 4 维度检查
        "field_accuracy",
        "ucp_reference_correctness", 
        "severity_reasonableness",
        "missing_check"
      ]
    }
  },
  "fallback": {
    "on_planner_fail": "skip",        // Planner 失败时跳过
    "on_knowledge_fail": "skip",      // Knowledge 失败时跳过
    "on_reflection_fail": "use_original", // Reflection 失败时使用原结果
    "on_all_fail": "fallback_to_v2"   // 全部失败时回退到 V2
  }
}
```

---

## 🔄 版本演进

| 版本 | 时间 | 核心特性 |
|------|------|----------|
| V1.0 | 早期 | 基础 OCR + 规则审核 |
| **V2.0** | 上一版 | OCR + RAG + LLM 单路审核 |
| **V3.0** | 本次更新 | **Multi-Agent + 知识增强 + 对比学习** |

---

## 🛡️ 容错机制

V3.0 设计了完善的容错体系：

```
用户请求
    │
    ▼
┌─────────────────┐
│ 尝试 V3 流程    │
│ (Multi-Agent)   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
  成功       失败
    │         │
    ▼         ▼
 返回结果  降级到 V2
           (原始流程)
                │
                ▼
             返回结果
```

---

## 🤝 贡献指南

V3.0 新增模块的贡献方式：

1. **对比学习数据**：向 `contrastive_data/` 添加标注示例
2. **Agent 优化**：在 `agent_enhance/` 中改进智能体逻辑
3. **提示词优化**：在 `agent_enhance/prompts/` 中优化提示词
4. **配置扩展**：在 `config/agent_config.json` 中添加新配置项

---

## 📄 许可证

本项目仅供学习和研究使用。

---

## 📮 更新日志

### V3.0 (2024-03)

- ✨ **新增** Multi-Agent 架构（Planner + Knowledge + Reflection）
- ✨ **新增** 知识增强预理解机制
- ✨ **新增** 4 维度反思纠错
- ✨ **新增** 对比学习数据集（700+ 示例）
- ✨ **新增** 结构化输出校验与自动修复
- ✨ **新增** 灵活 JSON 配置系统
- ✨ **新增** 完善的容错与降级机制
- ✨ **新增** 测试工具集（召回率测试、版本对比）
- ♻️ **优化** 保留 V2 全部功能作为降级备份

---

**一键恢复命令：**
```bash
curl -fsSL https://raw.githubusercontent.com/ZtongLi/The-LC-Checker/main/restore.sh | bash
```
