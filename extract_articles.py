#!/usr/bin/env python3
"""
从 ucp600quanwen.md 提取指定条款到单独文件
"""
import re
import os

# 中文数字映射
NUM_TO_CHINESE = {
    1: '一', 2: '二', 3: '三', 4: '四', 5: '五',
    6: '六', 7: '七', 8: '八', 9: '九', 10: '十',
    11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五',
    16: '十六', 17: '十七', 18: '十八', 19: '十九', 20: '二十',
    21: '二十一', 22: '二十二', 23: '二十三', 24: '二十四', 25: '二十五',
    26: '二十六', 27: '二十七', 28: '二十八', 29: '二十九', 30: '三十',
    31: '三十一', 32: '三十二', 33: '三十三', 34: '三十四', 35: '三十五',
    36: '三十六', 37: '三十七', 38: '三十八', 39: '三十九',
}

def num_to_chinese(num):
    return NUM_TO_CHINESE.get(num, str(num))

# 读取完整的 UCP600 文件
with open("ucp600quanwen.md", "r", encoding="utf-8") as f:
    content = f.read()

# 要提取的条款列表
articles_to_extract = [
    (3, "interpretation", "解释"),
    (4, "credit_vs_contract", "信用证与合同"),
    (6, "availability_expiry", "兑用方式、截止日和交单地点"),
    (7, "issuing_bank_obligation", "开证行责任"),
    (10, "amendments", "修改"),
    (17, "original_documents", "正本单据及副本"),
    (21, "non_negotiable_sea_waybill", "不可转让的海运单"),
    (22, "charter_party_bl", "租船合同提单"),
    (26, "on_deck_shippers_load", "货装舱面、托运人装载和计数"),
    (30, "tolerance", "信用证金额、数量与单价的伸缩度"),
    (31, "partial_shipment", "部分支款或部分发运"),
    (32, "installment", "分期支款或分期发运"),
    (33, "presentation_period", "交单时间"),
    (38, "transferable_credit", "可转让信用证"),
]

# 条款输出目录
output_dir = "knowledge_base/ucp600"
os.makedirs(output_dir, exist_ok=True)

# 构建所有条款的正则表达式模式
# 匹配 "第XX条 " 开头的行
chinese_nums_pattern = '|'.join(NUM_TO_CHINESE.values())
article_pattern = rf'第({chinese_nums_pattern})条\s+'

# 找到所有条款的位置
print("分析文件结构...")
matches = list(re.finditer(article_pattern, content))
print(f"找到 {len(matches)} 个条款标记")

# 构建中文数字到阿拉伯数字的映射
chinese_to_num = {v: k for k, v in NUM_TO_CHINESE.items()}

# 构建位置映射表
article_positions = {}
for i, match in enumerate(matches):
    # 提取中文数字
    ch_num = match.group(1)
    arab_num = chinese_to_num.get(ch_num)
    if arab_num:
        start_pos = match.start()
        # 结束位置是下一个条款的开始，或者是文件末尾
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)
        article_positions[arab_num] = (start_pos, end_pos)

print(f"识别到 {len(article_positions)} 个有效条款")

print("\n开始提取目标条款...")

# 为每个目标条款提取内容
for num, filename_suffix, chinese_name in articles_to_extract:
    if num not in article_positions:
        ch_num = num_to_chinese(num)
        print(f"❌ 未找到 Article {num} (第{ch_num}条)")
        continue
    
    start_pos, end_pos = article_positions[num]
    
    # 提取条款内容
    article_content = content[start_pos:end_pos].strip()
    
    # 生成文件名
    filename = f"article_{num:02d}_{filename_suffix}.txt"
    filepath = os.path.join(output_dir, filename)
    
    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(article_content)
    
    # 显示前80字符作为预览
    preview = article_content[:80].replace('\n', ' ')
    print(f"✅ Article {num:02d}: {filename} ({len(article_content)} 字符)")

print("\n提取完成！")

# 列出当前目录所有文件
files = sorted(os.listdir(output_dir))
print(f"\n当前知识库文件列表（共 {len(files)} 个）：")
for f in files:
    filepath = os.path.join(output_dir, f)
    size = os.path.getsize(filepath)
    # 检查文件是否有效（至少包含条款内容）
    with open(filepath, 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()
    print(f"  {f}: {size} bytes - {first_line[:40]}...")
