import os
import glob

def check_my_data():
    base_path = "./data"
    # This looks for any mp3 file inside any subfolder of 'ai' or 'human'
    files = glob.glob(os.path.join(base_path, "**", "*.mp3"), recursive=True)
    
    print(f"--- Data Integrity Check ---")
    print(f"Total MP3 files found: {len(files)}")
    
    # Check for specific languages detected
    languages = set()
    for f in files:
        # Extracts 'tamil' from 'data/ai/tamil/file.mp3'
        parts = f.split(os.sep)
        if len(parts) >= 3:
            languages.add(parts[-2])
            
    print(f"Languages detected: {', '.join(languages)}")
    
    if len(files) == 0:
        print("❌ ERROR: No files found. Check if your 'data' folder is in the same directory as this script.")
    else:
        print("✅ SUCCESS: Data is indexed and ready for training.")

if __name__ == "__main__":
    check_my_data()