# 信用证智能审单系统 (LC Checker)

[![Docker](https://img.shields.io/badge/Docker-Supported-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-orange)](https://fastapi.tiangolo.com/)

> 基于 OCR + RAG + LLM 的智能信用证单据审核平台

---

## 📖 项目介绍

**信用证智能审单系统**是一款面向国际贸易领域的 AI 辅助审单工具，帮助银行、进出口企业快速审核信用证及相关单据的一致性和合规性。

### 核心功能

| 功能模块 | 说明 |
|---------|------|
| 📄 **智能 OCR** | 自动识别信用证、发票、提单、保险单等单据 |
| 🔍 **规则审核** | 基于 UCP600 国际惯例的自动规则检查 |
| 🤖 **AI 审核** | 大语言模型全面审核，发现隐藏风险点 |
| 📊 **报告生成** | 自动生成标准化审核报告，支持导出 |

### 技术架构

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   React     │    │   FastAPI   │    │  PaddleOCR  │
│   前端      │ ←→ │   后端      │ ←→ │  文字识别   │
└─────────────┘    └─────────────┘    └─────────────┘
                          ↓
                   ┌─────────────┐    ┌─────────────┐
                   │  ChromaDB   │    │   OpenAI    │
                   │  向量数据库  │    │   大模型    │
                   └─────────────┘    └─────────────┘
```

### 支持的单据类型

- ✅ 信用证 (Letter of Credit)
- ✅ 商业发票 (Commercial Invoice)
- ✅ 提单 (Bill of Lading)
- ✅ 保险单 (Insurance Policy)

---

## 🚀 快速开始（一键恢复）

### 方式一：使用自动恢复脚本（推荐）

在新服务器上执行一行命令即可：

```bash
curl -fsSL https://raw.githubusercontent.com/ZtongLi/The-LC-Checker/main/restore.sh | bash
```

脚本会自动完成：
1. 克隆代码仓库
2. 安装 Docker 依赖（如未安装）
3. 配置环境变量
4. 构建并启动服务
5. 重建知识库（如需要）

### 方式二：手动部署

```bash
# 1. 克隆代码
git clone https://github.com/ZtongLi/The-LC-Checker.git
cd lc-checker

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填写你的 OpenAI API Key

# 3. 启动服务
docker-compose up -d

# 4. 访问服务
# 前端页面: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

---

## 📋 系统要求

| 资源 | 最低配置 | 推荐配置 |
|------|---------|---------|
| CPU | 2 核 | 4 核 |
| 内存 | 2 GB | 4 GB |
| 磁盘 | 10 GB | 20 GB |
| 网络 | 能访问外网 | 稳定外网 |

### 依赖环境

- [Docker](https://docs.docker.com/engine/install/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) 2.0+

---

## 🔧 配置说明

### 环境变量 (.env)

```bash
# OpenAI API 配置（用于 AI 审单功能）
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
```

### 数据持久化

以下目录会自动挂载为 Docker 卷，数据不会随容器删除而丢失：

| 目录 | 用途 |
|------|------|
| `./uploads/` | 用户上传的单据文件 |
| `./reports_v2/` | 生成的审核报告 |
| `./chroma_db/` | 向量数据库（可重建）|

---

## 💻 开发指南

### 本地开发（不使用 Docker）

```bash
# 后端
pip install -r requirements.txt
python server.py

# 前端
cd app
npm install
npm run dev
```

### 重建知识库

如果向量数据库损坏或需要更新：

```bash
# 在容器内执行
docker-compose exec lc-checker python build_knowledge_base.py

# 或本地执行
python build_knowledge_base.py
```

---

## 🧪 测试集

项目包含完整的测试数据集：

```
test_data/
├── test_cases.json          # 测试用例
test_pdf/
├── case_01_lc.pdf          # 信用证样本
├── case_01_invoice.pdf     # 发票样本
├── case_01_bl.pdf          # 提单样本
└── case_01_insurance.pdf   # 保险单样本
```

---

## 🐛 常见问题

### 服务启动失败

```bash
# 查看日志
docker-compose logs -f

# 检查端口占用
netstat -tlnp | grep 8000
```

### 知识库检索失败

```bash
# 重建知识库
docker-compose exec lc-checker python build_knowledge_base.py
```

### 首次启动较慢

首次启动需要下载模型（约 2GB），请耐心等待 3-5 分钟。

---

## 📁 项目结构

```
lc-checker/
├── app/                      # 前端 React 项目
│   ├── src/                  # 源代码
│   └── dist/                 # 构建产物
├── server.py                 # FastAPI 后端服务
├── check_v2.py               # 审核核心逻辑
├── ocr_extract.py            # OCR 文字提取
├── build_knowledge_base.py   # 知识库构建
├── knowledge_base/           # UCP600 知识库原文
├── test_data/                # 测试数据集
├── test_pdf/                 # 测试 PDF 样本
├── Dockerfile                # Docker 构建配置
├── docker-compose.yml        # Docker Compose 配置
├── restore.sh                # 一键恢复脚本
├── requirements.txt          # Python 依赖
└── README.md                 # 本文件
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目仅供学习和研究使用。

---

## 🙏 致谢

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - OCR 引擎
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [BGE-M3](https://huggingface.co/BAAI/bge-m3) - Embedding 模型
- [FastAPI](https://fastapi.tiangolo.com/) - Web 框架

---

## 📮 联系我们

如有问题或建议，欢迎通过 GitHub Issue 交流。

**一键恢复命令：**
```bash
curl -fsSL https://raw.githubusercontent.com/ZtongLi/The-LC-Checker/main/restore.sh | bash
```
