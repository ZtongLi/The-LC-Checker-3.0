#!/bin/bash
# ============================================
# 信用证智能审单系统 - 一键恢复脚本
# 在新服务器上执行此脚本即可完全恢复系统
# ============================================

set -e  # 遇到错误立即退出

# 配置变量（可根据需要修改）
REPO_URL="${REPO_URL:-https://github.com/yourusername/lc-checker.git}"
PROJECT_NAME="lc-checker"
COMPOSE_PROJECT_NAME="${PROJECT_NAME}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ============================================
# 检查依赖
# ============================================
check_dependencies() {
    log_info "检查系统依赖..."
    
    if ! command -v git &> /dev/null; then
        log_error "git 未安装，请先安装 git"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        log_warn "Docker 未安装，请先安装 Docker"
        echo "  Ubuntu/Debian: curl -fsSL https://get.docker.com | sh"
        echo "  或参考: https://docs.docker.com/engine/install/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_warn "Docker Compose 未安装，请先安装"
        echo "  Ubuntu/Debian: sudo apt install docker-compose-plugin"
        exit 1
    fi
    
    log_info "依赖检查通过"
}

# ============================================
# 克隆代码
# ============================================
clone_repository() {
    log_info "克隆代码仓库..."
    
    if [ -d "$PROJECT_NAME" ]; then
        log_warn "目录 $PROJECT_NAME 已存在"
        read -p "是否删除并重新克隆? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$PROJECT_NAME"
        else
            log_info "使用现有代码..."
            cd "$PROJECT_NAME"
            git pull
            return
        fi
    fi
    
    git clone "$REPO_URL" "$PROJECT_NAME"
    cd "$PROJECT_NAME"
    log_info "代码克隆完成"
}

# ============================================
# 配置环境变量
# ============================================
setup_environment() {
    log_info "配置环境变量..."
    
    if [ ! -f .env ]; then
        log_warn "未找到 .env 文件，创建默认配置"
        
        # 提示用户输入配置
        echo "请配置 OpenAI API 信息（用于 AI 审单功能）:"
        read -p "OpenAI API Key (直接回车使用本地 Ollama): " api_key
        read -p "OpenAI API Base (直接回车使用默认): " api_base
        read -p "OpenAI Model (默认 gpt-4o): " model
        
        # 创建 .env 文件
        cat > .env << EOF
# OpenAI API 配置
OPENAI_API_KEY=${api_key:-}
OPENAI_API_BASE=${api_base:-https://api.openai.com/v1}
OPENAI_MODEL=${model:-gpt-4o}

# 工作目录（容器内使用，无需修改）
WORK_DIR=/app
EOF
        
        log_info ".env 文件已创建"
        echo "  如需修改配置，请编辑 .env 文件"
    else
        log_info ".env 文件已存在，跳过配置"
    fi
}

# ============================================
# 创建必要目录
# ============================================
create_directories() {
    log_info "创建运行时目录..."
    
    mkdir -p uploads reports_v2 chroma_db
    
    log_info "目录创建完成"
}

# ============================================
# 构建并启动 Docker 容器
# ============================================
start_services() {
    log_info "构建 Docker 镜像..."
    
    # 检查 docker compose 命令格式
    if docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
    else
        COMPOSE_CMD="docker-compose"
    fi
    
    # 构建镜像
    $COMPOSE_CMD build --no-cache
    
    log_info "启动服务..."
    $COMPOSE_CMD up -d
    
    log_info "等待服务启动..."
    sleep 5
    
    # 检查服务健康状态
    log_info "检查服务健康状态..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
            log_info "服务已就绪！"
            return 0
        fi
        echo -n "."
        sleep 2
    done
    
    log_warn "服务启动可能未完成，请手动检查日志: $COMPOSE_CMD logs -f"
}

# ============================================
# 显示使用信息
# ============================================
show_usage() {
    echo ""
    echo "========================================"
    echo "  信用证智能审单系统部署完成！"
    echo "========================================"
    echo ""
    echo "  访问地址: http://localhost:8000"
    echo "  API 文档: http://localhost:8000/docs"
    echo "  健康检查: http://localhost:8000/api/health"
    echo ""
    echo "  常用命令:"
    echo "    查看日志: docker-compose logs -f"
    echo "    停止服务: docker-compose down"
    echo "    重启服务: docker-compose restart"
    echo ""
    echo "  如需重建知识库:"
    echo "    docker-compose exec lc-checker python build_knowledge_base.py"
    echo ""
    echo "========================================"
}

# ============================================
# 主函数
# ============================================
main() {
    echo "========================================"
    echo "  信用证智能审单系统 - 一键恢复"
    echo "========================================"
    echo ""
    
    # 如果提供了自定义仓库地址
    if [ -n "$1" ]; then
        REPO_URL="$1"
    fi
    
    log_info "使用仓库地址: $REPO_URL"
    
    check_dependencies
    clone_repository
    setup_environment
    create_directories
    start_services
    show_usage
}

# 执行主函数
main "$@"
