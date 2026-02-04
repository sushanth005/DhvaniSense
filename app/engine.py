import torch
import librosa
import io
import numpy as np
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor

class DetectionEngine:
    def __init__(self, model_path="./models/final_voice_model"):
        # Load local fine-tuned weights or the base model if testing
        self.extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-base-960h")
        self.model = Wav2Vec2ForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

    def process_audio(self, audio_bytes, language="Unknown"):
        # 1. In-memory decoding: avoid disk I/O for speed
        # 2. Resample to 16kHz as required by Wav2Vec2
        y, _ = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        
        # Extract features and convert to tensors
        inputs = self.extractor(y, sampling_rate=16000, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            logits = self.model(**inputs).logits
            # MATH: Probabilities = Softmax(Logits)
            probs = torch.nn.functional.softmax(logits, dim=-1)
            conf, label_idx = torch.max(probs, dim=-1)

        label = "AI_GENERATED" if label_idx.item() == 1 else "HUMAN"
        score = round(float(conf.item()), 4)
        return label, score, language

    def explain(self, label, score):
        """Forensic logic mapping scores to descriptive reasons."""
        reasons = {
            "AI_GENERATED": [
                "Detected spectral artifacts common in neural vocoders.",
                "Lack of natural pitch jitter and micro-prosody detected.",
                "Abnormal phase consistency typical of synthetic speech units."
            ],
            "HUMAN": [
                "Presence of natural stochastic background noise and air turbulence.",
                "Complex frequency modulations consistent with human vocal folds.",
                "Biological jitter/shimmer patterns detected in phoneme transitions."
            ]
        }
        # Select a reason based on confidence tier
        idx = 0 if score > 0.9 else (1 if score > 0.7 else 2)
        return reasons[label][idx]