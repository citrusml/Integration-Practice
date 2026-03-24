import os
import json
import random
import subprocess
import argparse

def generate_tex_content(problems, seed):
    tex_template = r"""\documentclass[12pt, a4paper]{ltjsarticle}
\usepackage{amsmath, amssymb}
\usepackage[margin=2cm]{geometry}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[R]{Seed: """ + str(seed) + r"""}
\fancyhead[L]{Integration Practice}

\begin{document}

\section*{Integration Problems}
\vspace{1cm}
\begin{enumerate}
"""
    
    # Add problems
    for item in problems:
        prob = item.get("problem", "")
        if prob is None: prob = ""
        
        # もしprobが配列（複数行）で渡された場合の処理
        if isinstance(prob, list):
            lines = " \\\\ \n      ".join(prob)
            prob = f"\\begin{{aligned}} \n      {lines} \n    \\end{{aligned}}"
            
        prob = prob.replace("$", "").replace("\\[", "").replace("\\]", "").strip()
            
        tex_template += f"    \\item $\\displaystyle {prob} $\n\\vspace{{2cm}}\n"
        
    tex_template += r"""\end{enumerate}

\newpage
\fancyhead[L]{Integration Practice - Answers}

\section*{Answers}
\vspace{1cm}
\begin{enumerate}
"""
    
    # Add answers
    for item in problems:
        ans = item.get("answer", "")
        if ans is None: ans = ""
        
        # もしansが配列（複数行）で渡された場合の処理
        if isinstance(ans, list):
            lines = " \\\\ \n      ".join(ans)
            ans = f"\\begin{{aligned}} \n      {lines} \n    \\end{{aligned}}"
            
        ans = ans.replace("$", "").replace("\\[", "").replace("\\]", "").strip()
        if ans:
            tex_template += f"    \\item $\\displaystyle {ans} $\n\\vspace{{1cm}}\n"
        else:
            tex_template += f"    \\item (Answer not available in DB)\n\\vspace{{1cm}}\n"
            
    tex_template += r"""\end{enumerate}
\end{document}
"""
    return tex_template

def main():
    parser = argparse.ArgumentParser(description="Generate PDF with random integration problems.")
    parser.add_argument("--count", type=int, default=1, help="Number of PDFs to generate")
    parser.add_argument("--seed", type=int, default=None, help="Specific seed (only applied to the first PDF if count=1)")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, "data", "database.json")
    out_dir = os.path.join(project_root, "results", "pdfs")
    os.makedirs(out_dir, exist_ok=True)
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}.")
        return

    with open(db_path, "r", encoding="utf-8") as f:
        database = json.load(f)
        
    all_problems = []
    for entry in database:
        all_problems.extend(entry.get("items", []))
        
    problems_a = [p for p in all_problems if p.get("tag") == "A"]
    problems_b = [p for p in all_problems if p.get("tag") == "B"]
    problems_c = [p for p in all_problems if p.get("tag") == "C"]
        
    if len(problems_a) < 2 or len(problems_b) < 3 or len(problems_c) < 3:
        print(f"Not enough tagged problems in DB.")
        print(f"Need A:2, B:3, C:3. Found A:{len(problems_a)}, B:{len(problems_b)}, C:{len(problems_c)}.")
        return

    for i in range(args.count):
        current_seed = args.seed if args.seed is not None and i == 0 else random.randint(1000, 9999)
        random.seed(current_seed)
        
        selected = random.sample(problems_a, 2) + random.sample(problems_b, 3) + random.sample(problems_c, 3)
        
        tex_content = generate_tex_content(selected, current_seed)
        
        tex_file = os.path.join(out_dir, f"practice_{current_seed}.tex")
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(tex_content)
            
        print(f"Generating PDF for seed {current_seed}...")
        try:
            # We must specify output-directory so pdflatex knows where to write the auxiliary files
            subprocess.run(
                ["lualatex", "-interaction=nonstopmode", "-output-directory", out_dir, tex_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            print(f"Created {tex_file.replace('.tex', '.pdf')}")
        except subprocess.CalledProcessError:
            print(f"Failed to generate PDF from {tex_file}")

if __name__ == "__main__":
    main()
