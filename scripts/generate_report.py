import os
import glob
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from app.engine import DetectionEngine

def run_multilingual_validation():
    print("🧪 Initializing Multilingual Forensic Validation...")
    detector = DetectionEngine()
    
    results = []
    # Index all files
    all_files = glob.glob("data/**/*.mp3", recursive=True)
    
    print(f"📂 Found {len(all_files)} files. Starting inference...")

    for file_path in all_files:
        # Extract metadata from path: data/{label}/{language}/{filename}
        parts = file_path.split(os.sep)
        true_label = parts[1].upper() if parts[1] == 'human' else 'AI_GENERATED'
        language = parts[2]

        try:
            # We read the file as bytes to simulate the API behavior
            with open(file_path, "rb") as f:
                audio_bytes = f.read()
            
            pred_label, score = detector.process_audio(audio_bytes)
            
            results.append({
                "Language": language,
                "True_Label": true_label,
                "Pred_Label": pred_label,
                "Score": score,
                "Correct": 1 if true_label == pred_label else 0
            })
        except Exception as e:
            print(f"⚠️ Skip {file_path}: {e}")

    # Create Analysis DataFrame
    df = pd.DataFrame(results)

    # 1. Overall Metrics
    print("\n" + "="*40)
    print("📊 GLOBAL PERFORMANCE REPORT")
    print("="*40)
    print(classification_report(df['True_Label'], df['Pred_Label']))

    # 2. Per-Language Accuracy
    print("\n🌍 ACCURACY BY LANGUAGE:")
    lang_acc = df.groupby('Language')['Correct'].mean() * 100
    print(lang_acc.to_string(float_format="{:,.2f}%".format))

    # 3. Export for your records
    df.to_csv("validation_results.csv", index=False)
    print("\n✅ Full detailed report saved to 'validation_results.csv'")

if __name__ == "__main__":
    run_multilingual_validation()