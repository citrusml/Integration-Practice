import os
import glob
import shutil

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdfs_dir = os.path.join(project_root, "results", "pdfs")
    
    # GitHub Pages用に docs ディレクトリを作成
    docs_dir = os.path.join(project_root, "docs")
    docs_pdfs_dir = os.path.join(docs_dir, "pdfs")
    os.makedirs(docs_pdfs_dir, exist_ok=True)
    
    # Get all practice PDFs
    pdf_files = sorted(glob.glob(os.path.join(pdfs_dir, "practice_*.pdf")))
    
    cards_html = ""
    for i, filepath in enumerate(pdf_files):
        filename = os.path.basename(filepath)
        seed = filename.replace("practice_", "").replace(".pdf", "")
        
        # GitHub Pagesで公開できるように、PDFを docs/pdfs/ にコピーする
        shutil.copy2(filepath, os.path.join(docs_pdfs_dir, filename))
        
        rel_path = f"./pdfs/{filename}"
        
        cards_html += f"""
        <div class="card">
            <div class="card-header">
                <h3>Practice #{i+1}</h3>
                <span class="seed-badge">Seed: {seed}</span>
            </div>
            <div class="card-body">
                <p>1 page of Problems, 1 page of Answers</p>
                <div class="card-actions">
                    <a href="{rel_path}" target="_blank" class="btn btn-outline">View</a>
                    <a href="{rel_path}" download="{filename}" class="btn btn-primary">Download</a>
                </div>
            </div>
        </div>
        """

        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Integration Practice PDFs</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #4F46E5;
            --primary-hover: #4338CA;
            --bg-color: #F9FAFB;
            --card-bg: rgba(255, 255, 255, 0.85);
            --text-main: #1F2937;
            --text-muted: #6B7280;
            --border-color: #E5E7EB;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2rem;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-top: 2rem;
        }}
        
        h1 {{
            font-size: 3rem;
            font-weight: 700;
            background: -webkit-linear-gradient(45deg, #4F46E5, #EC4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        p.subtitle {{
            font-size: 1.1rem;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        
        .card {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: rgba(79, 70, 229, 0.3);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .card-header h3 {{
            font-size: 1.25rem;
            font-weight: 600;
        }}
        
        .seed-badge {{
            background: #EEF2FF;
            color: var(--primary);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .card-body p {{
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
        }}
        
        .card-actions {{
            display: flex;
            gap: 0.75rem;
            margin-top: auto;
        }}
        
        .btn {{
            flex: 1;
            display: inline-block;
            text-align: center;
            padding: 0.6rem 1rem;
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.95rem;
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
        }}
        
        .btn-primary {{
            background-color: var(--primary);
            color: white;
            border: 1px solid var(--primary);
        }}
        
        .btn-primary:hover {{
            background-color: var(--primary-hover);
            box-shadow: 0 0 15px rgba(79, 70, 229, 0.4);
        }}
        
        .btn-outline {{
            background-color: transparent;
            color: var(--primary);
            border: 1px solid var(--primary);
        }}
        
        .btn-outline:hover {{
            background-color: #EEF2FF;
        }}
        
        footer {{
            text-align: center;
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-muted);
        }}
    </style>
</head>
<body>
    <header>
        <h1>Integration Practice Hub</h1>
        <p class="subtitle">Download randomly generated integration problem sets. Each PDF contains 8 problems selected from different difficulty categories, complete with step-by-step solutions on the second page.</p>
    </header>
    
    <div class="container">
        <div class="grid">
            {cards_html}
        </div>
    </div>
    
    <footer>
        <p>&copy; 2026 Integration Practice Project. Generated via Python and LuaLaTeX.</p>
    </footer>
</body>
</html>
"""
    
    index_file = os.path.join(docs_dir, "index.html")
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Successfully generated GitHub Pages compatible site at {index_file} with {len(pdf_files)} PDF links.")

if __name__ == "__main__":
    main()
