import json
import os
import subprocess

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, "data", "database.json")
    out_dir = os.path.join(project_root, "results", "pdfs")
    os.makedirs(out_dir, exist_ok=True)
    
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    all_problems = []
    for entry in data:
        all_problems.extend(entry.get("items", []))
        
    tex_template = r"""\documentclass[11pt, a4paper]{ltjsarticle}
\usepackage{amsmath, amssymb}
\usepackage[margin=1.5cm]{geometry}
\usepackage{fancyhdr}
\usepackage{enumitem}
\pagestyle{fancy}
\fancyhead[R]{Total: """ + str(len(all_problems)) + r""" Problems}
\fancyhead[L]{Integration Practice - Full List}

\begin{document}

\section*{All Problems and Answers (目視確認用)}
\begin{enumerate}[label=\textbf{\arabic*.}]
"""
    
    for item in all_problems:
        prob = item.get("problem", "")
        if prob is None: prob = ""
        if isinstance(prob, list):
            lines = " \\\\ \n      ".join(prob)
            prob = f"\\begin{{aligned}} \n      {lines} \n    \\end{{aligned}}"
        prob = prob.replace("$", "").replace("\\[", "").replace("\\]", "").strip()
        
        ans = item.get("answer", "")
        if ans is None: ans = ""
        if isinstance(ans, list):
            lines = " \\\\ \n      ".join(ans)
            ans = f"\\begin{{aligned}} \n      {lines} \n    \\end{{aligned}}"
        ans = ans.replace("$", "").replace("\\[", "").replace("\\]", "").strip()
        if not ans:
            ans = "\\text{(No Answer)}"
            
        tex_template += f"    \\item \n    \\textbf{{[Problem({item.get('tag', 'None')})]}} $\\displaystyle {prob} $ \\\\\n"
        tex_template += f"    \\textbf{{[Answer]}} $\\displaystyle {ans} $\n    \\vspace{{0.8cm}}\n"
        
    tex_template += r"""\end{enumerate}
\end{document}
"""
    
    tex_file = os.path.join(out_dir, "all_problems.tex")
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(tex_template)
        
    print("Compiling all_problems.tex...")
    subprocess.run(
        ["lualatex", "-interaction=nonstopmode", "-output-directory", out_dir, tex_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )
    print(f"Successfully generated results/pdfs/all_problems.pdf")

if __name__ == "__main__":
    main()
