import json

with open('标注数据_reformated (1).json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"数据类型: {type(data)}")
print(f"题目数量: {len(data)}")
print(f"\n第一道题的字段:")
for key in data[0].keys():
    print(f"  - {key}")

print(f"\n第一道题示例:")
first = data[0]
print(f"标注人: {first.get('标注人')}")
print(f"模型: {first.get('teacher_model')}")
print(f"问题: {first.get('question')[:100]}...")
print(f"评分标准数量: {len(json.loads(first.get('evaluation_rubric', '[]')))}")

print(f"\n前5道题的问题:")
for i, item in enumerate(data[:5], 1):
    q = item.get('question', '')
    print(f"{i}. {q[:80]}...")
