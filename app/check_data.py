import os
import glob

def verify_folders(root_dir="./data"):
    categories = ["ai", "human"]
    print(f"🔍 Checking directory: {os.path.abspath(root_dir)}")
    
    for cat in categories:
        path = os.path.join(root_dir, cat)
        if not os.path.exists(path):
            print(f"❌ Missing folder: {path}")
            continue
            
        # Count all mp3s in subfolders (Tamil, Telugu, etc.)
        files = glob.glob(os.path.join(path, "**", "*.mp3"), recursive=True)
        languages = set(os.path.basename(os.path.dirname(f)) for f in files)
        
        print(f"✅ Found {len(files)} files in '{cat}' across languages: {', '.join(languages)}")

if __name__ == "__main__":
    verify_folders()