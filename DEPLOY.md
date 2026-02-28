# 信用证智能审单系统 - Docker 部署指南

## 📋 概述

本文档指导你如何将系统部署到 Docker，并在新服务器上一键恢复。

---

## 🚀 首次部署（当前服务器）

### 1. 上传到 GitHub

```bash
# 在本地执行
cd /root/lc-checker

# 初始化 Git 仓库（如未初始化）
git init
git add .
git commit -m "Initial Docker deployment"

# 推送到 GitHub（先创建好仓库）
git remote add origin https://github.com/yourusername/lc-checker.git
git push -u origin main
```

### 2. 配置环境变量

```bash
# 创建 .env 文件
cp .env.example .env  # 或直接编辑

# 编辑 .env，填写你的 OpenAI API 配置
nano .env
```

`.env` 文件示例：
```bash
# OpenAI API 配置（必填）
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
```

### 3. 启动服务

```bash
# 使用 Docker Compose 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 等待服务启动完成（约 1-2 分钟）
```

### 4. 验证部署

访问以下地址检查服务状态：
- 前端页面: http://你的服务器IP:8000
- API 文档: http://你的服务器IP:8000/docs
- 健康检查: http://你的服务器IP:8000/api/health

---

## 🔄 迁移到新服务器（一键恢复）

### 方式一：使用恢复脚本（推荐）

在新服务器上执行：

```bash
# 1. 下载恢复脚本
curl -fsSL https://raw.githubusercontent.com/yourusername/lc-checker/main/restore.sh -o restore.sh
chmod +x restore.sh

# 2. 执行恢复（会自动克隆代码、配置环境、启动服务）
./restore.sh https://github.com/yourusername/lc-checker.git
```

或简化为：
```bash
curl -fsSL https://your-domain.com/restore.sh | bash -s -- https://github.com/yourusername/lc-checker.git
```

### 方式二：手动恢复

```bash
# 1. 克隆代码
git clone https://github.com/yourusername/lc-checker.git
cd lc-checker

# 2. 配置环境
cp .env.example .env
nano .env  # 填写 API Key

# 3. 创建目录
mkdir -p uploads reports_v2 chroma_db

# 4. 启动服务
docker-compose up -d
```

---

## 📁 数据持久化说明

| 目录 | 用途 | 备份建议 |
|------|------|---------|
| `uploads/` | 用户上传的文件 | ⚠️ 如需保留历史数据，需备份 |
| `reports_v2/` | 生成的审核报告 | ⚠️ 如需保留历史报告，需备份 |
| `chroma_db/` | 向量数据库 | ❌ 可重建，首次启动会自动生成 |
| `knowledge_base/` | UCP600 知识库原文 | ✅ 已包含在代码中 |
| `test_data/` | 测试数据集 | ✅ 已包含在代码中 |

### 备份数据

```bash
# 备份上传文件和报告
tar czvf lc-checker-data-backup.tar.gz uploads/ reports_v2/

# 恢复数据（新服务器）
tar xzvf lc-checker-data-backup.tar.gz
```

---

## 🔧 常用命令

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 停止并删除所有数据（包括卷）
docker-compose down -v

# 进入容器内部
docker-compose exec lc-checker bash

# 重建知识库（如需更新）
docker-compose exec lc-checker python build_knowledge_base.py

# 更新代码后重新构建
git pull
docker-compose up -d --build
```

---

## ⚠️ 注意事项

### 1. 首次启动较慢

首次启动时，Docker 需要：
- 构建镜像（约 3-5 分钟）
- 下载 PaddleOCR 模型（约 100MB，自动完成）
- 加载 SentenceTransformer 模型（约 2GB，自动完成）

请耐心等待，可通过日志查看进度：
```bash
docker-compose logs -f
```

### 2. 知识库重建

如果 `chroma_db/` 目录为空或损坏，可以重建：
```bash
docker-compose exec lc-checker python build_knowledge_base.py
```

### 3. 内存要求

- **最低配置**: 2GB 内存
- **推荐配置**: 4GB 内存（确保 SentenceTransformer 模型加载顺畅）

### 4. 端口冲突

如果 8000 端口被占用，修改 `docker-compose.yml`：
```yaml
ports:
  - "8080:8000"  # 改为 8080 或其他端口
```

---

## 🐛 故障排查

### 服务无法启动

```bash
# 检查日志
docker-compose logs --tail=100

# 检查端口占用
netstat -tlnp | grep 8000
```

### ChromaDB 连接失败

```bash
# 进入容器检查
docker-compose exec lc-checker ls -la chroma_db/

# 重建知识库
docker-compose exec lc-checker python build_knowledge_base.py
```

### 前端页面无法访问

```bash
# 检查前端文件是否存在
docker-compose exec lc-checker ls -la app/dist/

# 如果缺少，需要构建前端
cd app && npm install && npm run build
```

---

## 📚 技术栈

- **后端**: Python + FastAPI
- **前端**: React + Vite + TypeScript
- **OCR**: PaddleOCR
- **向量数据库**: ChromaDB + BGE-M3
- **LLM**: OpenAI API / Ollama

---

## 💡 提示

1. **GitHub 仓库** 只保存代码和测试数据，不保存运行时数据
2. **换服务器时**，只需执行 `restore.sh` 即可恢复
3. **实验数据**（测试集）已包含在代码中，会随 Git 一起迁移
4. **用户上传的文件**如需保留，请单独备份 `uploads/` 目录
