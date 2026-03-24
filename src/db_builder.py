import os
import sys
import json
import glob
import time

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
        print("Error: GEMINI_API_KEY is not set.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(project_root, "images")
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    image_files = sorted(glob.glob(os.path.join(images_dir, "*.JPG")))
    if not image_files:
        print(f"No JPG files found in {images_dir}")
        sys.exit(1)
        
    database = []
    out_file = os.path.join(data_dir, "database.json")
    
    # Load existing to resume if needed
    if os.path.exists(out_file):
        try:
            with open(out_file, "r", encoding="utf-8") as f:
                database = json.load(f)
        except json.JSONDecodeError:
            pass
            
    processed_images = {entry["image_filename"] for entry in database}
    
    prompt = r"""
あなたはデータ化の専門家です。
提供された画像には、1つあるいは複数の、積分計算の「問題」や「解答・途中式」が含まれています。
画像から【すべての問題】と【対応する解答】を抽出して、以下のスキーマに従ったJSON文字列のみを出力してください。
解答が見当たらない問題については、"answer"項目をnullにしてください。
マークダウンブロック（```json など）は絶対に含めず、純粋なJSON文字列だけを返してください。数式は必ずLaTeX形式（$$ や \( \) など）を使用してください。

出力フォーマット：
[
  {
    "problem": "問題の数式（LaTeX形式）",
    "answer": "解答や途中式の数式（LaTeX形式、なければnull）"
  }
]
"""
    
    for img_path in image_files:
        filename = os.path.basename(img_path)
        if filename in processed_images:
            print(f"Skipping {filename} (already processed)")
            continue
            
        print(f"Processing {filename}...")
        
        for attempt in range(5): # Retry loop
            try:
                img = Image.open(img_path)
                
                # Use gemini-2.5-flash for free tier compatibility and speed
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[prompt, img]
                )
                
                # Clean up the output if it has markdown ticks
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                
                try:
                    items = json.loads(text)
                    if not isinstance(items, list):
                        items = []
                    # ----- タグをランダムに付与 -----
                    import random
                    for item in items:
                        if "tag" not in item:
                            item["tag"] = random.choice(["A", "B", "C"])
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON for {filename}: {e}\nRaw output: {text}")
                    items = []
                    
                entry = {
                    "image_filename": filename,
                    "items": items
                }
                database.append(entry)
                
                # Save incremental progress
                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(database, f, indent=2, ensure_ascii=False)
                    
                print(f"Successfully extracted {len(items)} items from {filename}.")
                
                # Rate limit consideration
                time.sleep(15)
                break # Exit retry loop on success
                
            except Exception as e:
                print(f"Error processing {filename} (Attempt {attempt+1}): {e}")
                if attempt < 4:
                    print("Waiting 30 seconds before retrying...")
                    time.sleep(30)
                else:
                    print(f"Failed to process {filename} after 5 attempts. Exiting.")
                    sys.exit(1)
            
    print(f"\nFinished processing. Data saved to {out_file}")

if __name__ == "__main__":
    main()
