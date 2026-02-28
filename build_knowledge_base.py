import os
import chromadb
from sentence_transformers import SentenceTransformer

# ============================================================
# 第一部分：加载 Embedding 模型
# BGE-M3 模型会在第一次运行时自动下载（约 2GB）
# 下载完成后会缓存到本地，以后不需要重复下载
# ============================================================
print("正在加载 BGE-M3 Embedding 模型...")
print("（如果是第一次运行，需要下载约 2GB 的模型文件，请耐心等待）")
embed_model = SentenceTransformer("BAAI/bge-m3")
print("模型加载完成！\n")

# ============================================================
# 第二部分：读取 UCP600 条款文件
# ============================================================
# 获取脚本所在目录，支持相对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
knowledge_dir = os.path.join(SCRIPT_DIR, "knowledge_base", "ucp600")
documents = []    # 存放条款文本内容
metadatas = []    # 存放元数据（条款编号、文件名等）
ids = []          # 存放每个条款的唯一 ID

print("正在读取 UCP600 条款文件...")

# 遍历 ucp600 文件夹下所有 txt 文件
for filename in sorted(os.listdir(knowledge_dir)):
    if filename.endswith(".txt"):
        filepath = os.path.join(knowledge_dir, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if content:
            # 从文件名中提取条款编号，例如 article_18 → Article 18
            article_num = filename.replace(".txt", "").split("_")[1] if "_" in filename else "unknown"

            documents.append(content)
            metadatas.append({
                "source": filename,
                "article": f"Article {article_num}",
            })
            ids.append(f"ucp600_{filename.replace('.txt', '')}")

            print(f"  已读取：{filename}（{len(content)} 字符）")

print(f"\n共读取 {len(documents)} 个条款文件\n")

# ============================================================
# 第三部分：生成向量
# ============================================================
print("正在将条款文本转为向量...")
embeddings = embed_model.encode(documents, show_progress_bar=True)
embeddings_list = embeddings.tolist()
print("向量生成完成！\n")

# ============================================================
# 第四部分：存入 ChromaDB
# ============================================================
print("正在存入 ChromaDB 向量数据库...")

# 初始化 ChromaDB，数据保存在本地文件夹
db_path = os.path.join(SCRIPT_DIR, "chroma_db")
client = chromadb.PersistentClient(path=db_path)

# 如果已经存在同名集合，先删除（方便重复运行）
try:
    client.delete_collection("ucp600")
    print("  已删除旧的集合")
except Exception:
    pass

# 创建新集合
collection = client.create_collection(
    name="ucp600",
    metadata={"description": "UCP600 跟单信用证统一惯例条款"}
)

# 将文档、向量、元数据一起存入
collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings_list,
    metadatas=metadatas,
)

print(f"  成功存入 {collection.count()} 个条款到 ChromaDB")
print(f"  数据库保存路径：{db_path}")
print("\n知识库构建完成！")