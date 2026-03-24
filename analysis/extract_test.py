import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from google import genai
from PIL import Image

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set in the environment.")
        print("Please export GEMINI_API_KEY='your_api_key' or add it to a .env file.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    # Resolve the path to the image
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(project_root, "images", "IMG_2821.JPG")
    
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        
    if not os.path.exists(img_path):
        print(f"Error: Image {img_path} not found.")
        sys.exit(1)
        
    print(f"Loading image: {img_path}")
    try:
        img = Image.open(img_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)
    
    # We will use gemini-2.5-pro for vision tasks reliably.
    
    prompt = r"""
    あなたは優秀な数学のアシスタントです。
    この画像には積分計算の問題とその解答が含まれています。
    画像から「積分問題の式」と「その解答・途中計算プロセス」を抽出してください。
    数式はプレーンテキストではなく、必ずLaTeX形式（$$ や \( \) などのマークアップ）で記述してください。
    問題部分と解答部分をわかりやすく分けて出力してください。
    
    出力フォーマットの例：
    【問題】
    $$ \int ... dx $$
    
    【解答】
    $$ = ... $$
    $$ = ... $$
    """
    
    print("Sending request to Gemini API (This may take a few seconds)...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img]
        )
        print("\n" + "="*40)
        print("=== 抽出結果 ===")
        print("="*40)
        print(response.text)
        
        # Save the result to results/extract_result.md
        results_dir = os.path.join(project_root, "results")
        os.makedirs(results_dir, exist_ok=True)
        out_file = os.path.join(results_dir, "extract_result.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"\nSaved result to {out_file}")
            
    except Exception as e:
        print(f"Error calling API: {e}")

if __name__ == "__main__":
    main()
