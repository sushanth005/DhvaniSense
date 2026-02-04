import base64
from fastapi import FastAPI, Header, HTTPException
from app.engine import DetectionEngine
from pydantic import BaseModel

app = FastAPI()
detector = DetectionEngine() # This loads your model

class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

@app.post("/api/v1/detect")
async def detect_voice(request: VoiceRequest, x_api_key: str = Header(None)):
    # 1. API Key Check
    if x_api_key != "ds_live_8f2a1c9e7b4d3f0a1c9e8f2a1c9e7b4d":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        # 2. Decode the Base64 audio
        audio_bytes = base64.b64decode(request.audioBase64)

        # 3. Call your engine's actual method: 'process_audio'
        label, score, language = detector.process_audio(audio_bytes, request.language)
        
        # 4. Get the forensic explanation
        explanation = detector.explain(label, score)

        return {
            "status": "success",
            "language": language,
            "classification": label,
            "confidenceScore": score,
            "explanation": explanation
        }
    except Exception as e:
        # This catches any issues and reports them clearly
        raise HTTPException(status_code=500, detail=f"Inference Error: {str(e)}")