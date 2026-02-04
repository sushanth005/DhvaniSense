import os
import torch
import librosa
import glob
from transformers import (
    Wav2Vec2ForSequenceClassification, 
    Wav2Vec2FeatureExtractor, 
    TrainingArguments, 
    Trainer
)
from torch.utils.data import Dataset

class VoiceDetectionDataset(Dataset):
    def __init__(self, root_dir):
        self.samples = []
        self.extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-base-960h")
        self.label_map = {"human": 0, "ai": 1}

        # Crawl through data/{class}/{language}/*.mp3
        for label_name, label_idx in self.label_map.items():
            pattern = os.path.join(root_dir, label_name, "**", "*.mp3")
            files = glob.glob(pattern, recursive=True)
            for f in files:
                self.samples.append((f, label_idx))
        print(f"✅ Training on {len(self.samples)} samples.")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        # Standardize to 16kHz for Wav2Vec2
        audio, _ = librosa.load(path, sr=16000, duration=3.0) # 3 seconds is plenty for "vibe" detection
        
        inputs = self.extractor(
            audio, 
            sampling_rate=16000, 
            return_tensors="pt", 
            padding="max_length", 
            max_length=48000, # 16000 * 3s
            truncation=True
        )
        return {
            "input_values": inputs.input_values.squeeze(0),
            "labels": torch.tensor(label)
        }

def train():
    # Load model with 2 classification heads (Human, AI)
    model = Wav2Vec2ForSequenceClassification.from_pretrained(
        "facebook/wav2vec2-base-960h", 
        num_labels=2
    )

    dataset = VoiceDetectionDataset("./data")

    training_args = TrainingArguments(
        output_dir="./models/checkpoints",
        num_train_epochs=15,             # Enough cycles for small data
        per_device_train_batch_size=4,   # Low batch size for stability
        learning_rate=3e-5,              # Gentle learning rate
        warmup_steps=20,                 # Helps model settle on audio features
        save_strategy="epoch",           # Save model every epoch
        logging_steps=10,
        fp16=torch.cuda.is_available(),  # Auto-enable GPU speedup if available
        push_to_hub=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    print("🚀 Training starting... (Go grab a coffee ☕)")
    trainer.train()
    
    # Save the Final Production Model
    model.save_pretrained("./models/final_voice_model")
    print("✨ Model saved to ./models/final_voice_model")

if __name__ == "__main__":
    train()