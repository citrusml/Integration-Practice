import json
import os

db_path = "data/database.json"

with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

dummy_answer = "= \\frac{1}{4}x^4 + x^3 + \\frac{3}{2}x^2 + x + C"

count = 0
for entry in data:
    for item in entry.get("items", []):
        ans = item.get("answer")
        if isinstance(ans, list):
            item["answer"] = dummy_answer
            count += 1

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Reverted {count} answers to single line.")
