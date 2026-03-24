import os
import glob
try:
    from PyPDF2 import PdfMerger
except ImportError:
    print("PyPDF2 is not installed. Please install it using: pip install PyPDF2")
    exit(1)

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_pdfs_dir = os.path.join(project_root, "docs", "pdfs")
    
    # docs/pdfs内のpractice_xxxx.pdfを取得
    pdf_files = sorted(glob.glob(os.path.join(docs_pdfs_dir, "practice_*.pdf")))
    
    if not pdf_files:
        print("No practice PDFs found to combine.")
        return
        
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
        
    output_path = os.path.join(docs_pdfs_dir, "all_practices_combined.pdf")
    merger.write(output_path)
    merger.close()
    
    print(f"Successfully combined {len(pdf_files)} PDFs into {output_path}")

if __name__ == "__main__":
    main()
