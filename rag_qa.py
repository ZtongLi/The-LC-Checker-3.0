import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# ============================================================
# 第一部分：加载模型和数据库
# ============================================================
print("正在加载系统...\n")

# 加载 Embedding 模型（用于将问题转为向量）
embed_model = SentenceTransformer("BAAI/bge-m3")

# 连接 ChromaDB 向量数据库
chroma_client = chromadb.PersistentClient(path="/root/lc-checker/chroma_db")
collection = chroma_client.get_collection("ucp600")

# 连接本地 Ollama 大模型
llm_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

print(f"系统加载完成！知识库中共有 {collection.count()} 个条款\n")

# ============================================================
# 第二部分：定义 RAG 问答函数
# ============================================================
def rag_answer(question, top_k=3):
    """
    RAG 问答流程：
    1. 将问题转为向量
    2. 在知识库中检索最相关的条款
    3. 将条款 + 问题一起发送给大模型
    4. 返回大模型的回答
    """

    # 第一步：检索相关条款
    print(f"正在检索相关条款...")
    query_embedding = embed_model.encode([question]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
    )

    # 拼接检索到的条款内容
    retrieved_context = ""
    print(f"找到 {len(results['ids'][0])} 个相关条款：")
    for i in range(len(results["ids"][0])):
        article = results["metadatas"][0][i].get("article", "未知")
        source = results["metadatas"][0][i].get("source", "未知")
        distance = results["distances"][0][i]
        content = results["documents"][0][i]

        print(f"  {i+1}. {article}（{source}，相似度距离：{distance:.4f}）")
        retrieved_context += f"\n{'='*50}\n{article}：\n{content}\n"

    # 第二步：构建 Prompt
    system_prompt = """你是一位资深的信用证审单专家，精通 UCP600 和 ISBP745。

请严格根据下方提供的 UCP600 条款原文来回答问题。

回答要求：
1. 必须引用具体的条款编号（如 Article 14(a)、Article 18(c) 等）
2. 先给出明确结论，再展开分析
3. 如果提供的条款中没有相关内容，请明确说明"所提供的条款中未涉及此问题"
4. 使用中文回答"""

    user_prompt = f"""以下是检索到的 UCP600 相关条款：

{retrieved_context}

{'='*50}

用户问题：{question}

请根据以上条款回答。"""

    # 第三步：调用大模型
    print(f"\n正在生成回答...\n")
    response = llm_client.chat.completions.create(
        model="qwen2.5:14b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,  # 降低温度，让回答更严谨
    )

    return response.choices[0].message.content


# ============================================================
# 第三部分：测试 RAG 问答效果
# ============================================================
test_questions = [
    "商业发票金额超过信用证金额，银行应该如何处理？",
    "提单上的装船日期晚于信用证规定的最迟装运日期，这算不算不符点？",
    "银行发现单据存在不符点后，有多少天的时间来决定是否拒绝？具体流程是什么？",
    "商业发票上的货物描述与信用证中的描述不完全一致，但意思相近，这算不算不符点？",
    "保险单据的最低保险金额应该是多少？如果信用证没有规定保险金额怎么办？",
]

for i, question in enumerate(test_questions, 1):
    print("=" * 70)
    print(f"问题 {i}：{question}")
    print("=" * 70)

    answer = rag_answer(question)

    print("AI 回答：")
    print("-" * 70)
    print(answer)
    print("\n")

    # 每个问题���间暂停，避免 GPU 过载
    if i < len(test_questions):
        import time
        time.sleep(2)