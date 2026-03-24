import json
import os
import subprocess
import sys

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, "data", "database.json")
    
    # 1. Check JSON validity
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print("カンマの抜け漏れや、不要なカンマ、クォーテーションの閉じ忘れなどがJSON内にある可能性があります。")
        return
        
    print("✅ JSON file is valid syntax.")
    
    # 2. Check schema and collect all equations
    all_problems = []
    for entry in data:
        items = entry.get("items", [])
        for i, item in enumerate(items):
            tag = item.get("tag")
            if tag not in ["A", "B", "C"]:
                print(f"⚠️ Warning: Invalid or missing tag '{tag}' in {entry.get('image_filename')} item {i}")
            
            all_problems.append(item)
            
    print(f"Found {len(all_problems)} valid problem entries.")
    print("Compiling all problems via lualatex to detect LaTeX syntax errors...")
    
    # 3. Create a giant TeX file to test compilation
    sys.path.append(os.path.join(project_root, "src"))
    import pdf_generator
    
    try:
        tex_content = pdf_generator.generate_tex_content(all_problems, seed="VALIDATION")
    except Exception as e:
        print(f"Error generating TeX content: {e}")
        return
        
    out_dir = os.path.join(project_root, "results", "pdfs")
    os.makedirs(out_dir, exist_ok=True)
    tex_file = os.path.join(out_dir, "validation.tex")
    
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(tex_content)
        
    result = subprocess.run(
        ["lualatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", out_dir, tex_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ LaTeX compilation successful! No syntax errors found in any equations.")
    else:
        print("❌ LaTeX compilation failed. There is a LaTeX syntax error in the database.")
        print("Please check the following error snippet:")
        print("-" * 40)
        log_file = os.path.join(out_dir, "validation.log")
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                log_lines = f.readlines()
                for i, line in enumerate(log_lines):
                    if line.startswith("!"):
                        # Print previous line and next few lines for context
                        start = max(0, i - 2)
                        end = min(len(log_lines), i + 10)
                        for j in range(start, end):
                            print(log_lines[j].rstrip())
                        break

if __name__ == "__main__":
    main()
