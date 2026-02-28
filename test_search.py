import chromadb
from sentence_transformers import SentenceTransformer

# ============================================================
# 加载模型和数据库
# ============================================================
print("正在加载模型和数据库...\n")
embed_model = SentenceTransformer("BAAI/bge-m3")
client = chromadb.PersistentClient(path="/root/lc-checker/chroma_db")
collection = client.get_collection("ucp600")

print(f"数据库中共有 {collection.count()} 个条款\n")

# ============================================================
# 定义测试问题
# ============================================================
test_queries = [
    "商业发票金额超过信用证金额怎么办",
    "提单上的装船日期晚于信用证规定的最迟装运日",
    "银行发现不符点后应该怎么处理",
    "发票上的货物描述与信用证不一致",
    "保险单据的保险金额最低要求是多少",
    "银行审核单据的时间限制是多少天",
]

# ============================================================
# 逐个测试检索效果
# ============================================================
for i, query in enumerate(test_queries, 1):
    print("=" * 70)
    print(f"测试 {i}：{query}")
    print("=" * 70)

    # 将问题转为向量
    query_embedding = embed_model.encode([query]).tolist()

    # 在数据库中搜索最相似的 3 个条款
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(3, collection.count()),
    )

    # 打印搜索结果
    for j in range(len(results["ids"][0])):
        doc_id = results["ids"][0][j]
        distance = results["distances"][0][j]
        metadata = results["metadatas"][0][j]
        # 只显示前 200 个字符，避免输出太长
        doc_preview = results["documents"][0][j][:200]

        print(f"\n  排名 {j+1}：")
        print(f"  条款：{metadata.get('article', '未知')}")
        print(f"  来源：{metadata.get('source', '未知')}")
        print(f"  距离：{distance:.4f}（越小越相关）")
        print(f"  内容预览：{doc_preview}...")

    print()