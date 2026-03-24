import json
import os

db_path = "data/database.json"

with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

replacements = {
    r"\in_{-1}^{0}": r"\int_{-1}^{0}",
    r"\int_{0}^{\frac{\pi}{2} \frac{sin\theta}": r"\int_{0}^{\frac{\pi}{2}} \frac{sin\theta}",
    r"\frac{cos\theta}{\sqrt{1 + 2sin\theta} d\theta": r"\frac{cos\theta}{\sqrt{1 + 2sin\theta}} d\theta",
    r"\int_{0}^{\frac{\pi}{2} \frac{cosx}": r"\int_{0}^{\frac{\pi}{2}} \frac{cosx}",
    r"\-frac{1}{x}": r"-\frac{1}{x}",
    r"log(x+\sqrt{x^2+1} + C": r"log(x+\sqrt{x^2+1}) + C",
    r"^{\frac{3}{2]}": r"^{\frac{3}{2}}",
    r"log(e^x+1) C": r"log(e^x+1) + C",
    r"log(e^x + e^{-x} + C": r"log(e^x + e^{-x}) + C",
    r"\frac{x^2}{2}{(logx)^2 - logx + \frac{1}{2} + C": r"\frac{x^2}{2}\{(logx)^2 - logx + \frac{1}{2}\} + C",
    r"-\frac{\pi{2} - 1": r"-\frac{\pi}{2} - 1",
    r"log|\frac{x}{x + 2} + C": r"log|\frac{x}{x + 2}| + C",
    r"\frac{3}{2}(x - \frac{1}{2}log|2x + 1| + C": r"\frac{3}{2}(x - \frac{1}{2}log|2x + 1|) + C",
    r"log\frac{2 - \sqrt{3}cosx}{2 + \sqrt{3}cosx} C": r"log\frac{2 - \sqrt{3}cosx}{2 + \sqrt{3}cosx} + C"
}

count = 0
for entry in data:
    for item in entry.get("items", []):
        p = item.get("problem", "")
        a = item.get("answer", "")
        
        for k, v in replacements.items():
            if isinstance(p, str) and k in p:
                item["problem"] = item["problem"].replace(k, v)
                count += 1
            if isinstance(a, str) and k in a:
                item["answer"] = item["answer"].replace(k, v)
                count += 1
            if isinstance(a, list):
                new_a = []
                for line in a:
                    if k in line:
                        line = line.replace(k, v)
                        count += 1
                    new_a.append(line)
                item["answer"] = new_a

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Fixed {count} LaTeX syntax errors in database.json")
