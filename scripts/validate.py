import os
import glob
import torch
import librosa
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from app.engine import DetectionEngine  # Reuse your production logic

def run_benchmarks(data_root="./data"):
    detector = DetectionEngine()
    y_true = []
    y_pred = []
    
    print("🧪 Starting Multilingual Accuracy Validation...")
    
    # Mapping folders to labels
    categories = {"human": 0, "ai": 1}
    
    for label_str, label_idx in categories.items():
        # Crawl all language subfolders
        files = glob.glob(os.path.join(data_root, label_str, "**", "*.mp3"), recursive=True)
        
        for f_path in files:
            try:
                # 1. Load file
                with open(f_path, "rb") as f:
                    audio_bytes = f.read()
                
                # 2. Predict using production engine
                label, score = detector.analyze(audio_bytes)
                
                # 3. Store results
                y_true.append(label_idx)
                y_pred.append(1 if label == "AI_GENERATED" else 0)
                
            except Exception as e:
                print(f"⚠️ Error processing {f_path}: {e}")

    # 4. Final Calculation
    print("\n" + "="*30)
    print("📊 FINAL PERFORMANCE REPORT")
    print("="*30)
    print(classification_report(y_true, y_pred, target_names=["HUMAN", "AI_GENERATED"]))
    print(f"Overall Accuracy: {accuracy_score(y_true, y_pred):.4f}")

if __name__ == "__main__":
    run_benchmarks()