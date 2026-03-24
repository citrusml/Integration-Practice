import json
import random
import os

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, "data", "database.json")
    
    if not os.path.exists(db_path):
        print(f"No database found at {db_path}")
        return
        
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    updated = False
    for entry in data:
        for item in entry.get("items", []):
            if "tag" not in item:
                item["tag"] = random.choice(["A", "B", "C"])
                updated = True
                
    if updated:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Successfully added random tags to existing DB entries.")
    else:
        print("All entries already have tags.")

if __name__ == "__main__":
    main()
