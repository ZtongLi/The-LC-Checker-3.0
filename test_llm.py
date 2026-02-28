from openai import OpenAI

# 连接本地 Ollama 服务
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama 不需要真实的 API Key，随便填一个就行
)

# 向 Qwen2.5-14B 发送一个信用证相关的问题
response = client.chat.completions.create(
    model="qwen2.5:14b",
    messages=[
        {
            "role": "system",
            "content": "你是一位资深的信用证审单专家，精通 UCP600 和 ISBP745。"
        },
        {
            "role": "user",
            "content": "请简要解释 UCP600 第 14 条关于审核单据标准的主要内容，并举一个审单中的实际例子。"
        }
    ]
)

# 打印 AI 的回答
print("=" * 60)
print("AI 回答：")
print("=" * 60)
print(response.choices[0].message.content)