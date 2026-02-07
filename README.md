🎧 DhvaniSense - AI Voice Detector (Human vs AI Audio Classification API)

DhvaniSense is an AI-powered FastAPI backend project that detects whether a given audio sample is **AI-generated** or **Human-generated**.  
It supports `.mp3` audio inputs (and `.wav` optionally) and provides a production-ready API endpoint for real-time classification.

This project includes:
✅ Dataset checking  
✅ Training pipeline  
✅ Validation pipeline  
✅ Report generation  
✅ FastAPI server deployment  
✅ API + Client testing scripts  

---

# 🚀 Features

- 🎙️ Detect AI-generated vs Human voice from audio files
- ⚡ FastAPI backend with clean API endpoints
- 🔐 API Key authentication support
- 🧠 Model training + checkpoint saving
- 📊 Validation results exported into CSV
- 📄 Report generation supported
- 🐳 Docker support for deployment
- ☁️ Cloud deploy-ready (Google Cloud / Azure / AWS)
- 📥 Supports Base64 encoded audio request payload

---

# 🏗️ Project Workflow (Pipeline)

Follow the pipeline in this exact order:

requirements.txt
↓
test_paths.py
↓
app/check_data.py
↓
scripts/train_mini.py (takes time, creates models)
↓
scripts/validate.py
↓
scripts/generate_report.py
↓
uvicorn app.main:app
↓
app/test_api.py
↓
test_client.py


---

# 📁 Folder Structure

DhvaniSense/
│
├── app/
│ ├── pycache/
│ ├── init.py
│ ├── auth.py
│ ├── check_data.py
│ ├── engine.py
│ ├── main.py
│ ├── test_api.py
│ └── utils.py
│
├── data/
│ ├── ai/
│ └── human/
│
├── models/
│ ├── checkpoints/
│ ├── final_voice_model/
│ └── config.json
│
├── scripts/
│ ├── generate_report.py
│ ├── train_mini.py
│ └── validate.py
│
├── venv/ # Local virtual environment (not for GitHub)
│
├── .gitattributes
├── .gitignore
├── Dockerfile
├── requirements.txt
├── test_client.py
├── test_paths.py
└── validation_results.csv


---

# ⚙️ Requirements

- Python **3.10+**
- pip installed
- FFmpeg installed (**required for `.mp3` support**)

---

# 🔧 Installation Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/DhvaniSense.git
cd DhvaniSense
2️⃣ Create Virtual Environment
python -m venv venv
Activate it:

Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
🎵 MP3 Support (FFmpeg Required)
Since this project supports .mp3 audio, FFmpeg must be installed.

✅ Check FFmpeg Installation
ffmpeg -version
If it shows version details, you're good.

🪟 Install FFmpeg on Windows
Download FFmpeg from: https://ffmpeg.org/download.html

Extract the zip file

Add the bin/ folder to Windows Environment Variables (PATH)

Example:

C:\ffmpeg\bin
Restart terminal after adding PATH.

📌 Dataset Setup
Place your dataset in this exact format:

data/
  ├── ai/
  │     ├── sample1.mp3
  │     ├── sample2.mp3
  │     └── ...
  └── human/
        ├── sample1.mp3
        ├── sample2.mp3
        └── ...
Supported formats:

.mp3 ✅

.wav ✅

✅ Step-by-Step Execution (Correct Order)
✅ Step 1: Verify Paths
Run:

python test_paths.py
This ensures:

all directories exist

dataset paths are correct

models/scripts folders are present

✅ Step 2: Check Dataset
Run:

python app/check_data.py
This checks:

dataset folder validity

corrupted/unreadable audio files

missing audio samples

✅ Step 3: Train Model (Main Training Script)
Run:

python scripts/train_mini.py
⚠️ This step takes time depending on dataset size and system speed.

This generates model outputs inside:

models/final_voice_model/
models/checkpoints/
models/config.json
✅ Step 4: Validate Model
Run:

python scripts/validate.py
This generates:

validation_results.csv
✅ Step 5: Generate Report
Run:

python scripts/generate_report.py
This script generates a final evaluation report from validation results.

🌐 Run the FastAPI Server
Start the backend server using uvicorn:

uvicorn app.main:app --host 0.0.0.0 --port 8000
Server runs at:

http://127.0.0.1:8000
📑 API Documentation
Once the server is running, open:

Swagger UI
http://127.0.0.1:8000/docs
Redoc
http://127.0.0.1:8000/redoc
🔑 Authentication (API Key Support)
API key authentication logic is implemented in:

app/auth.py
Requests must include the header:

x-api-key: <YOUR_API_KEY>
📌 API Endpoints
✅ Health Check
GET

/health
Example response:

{
  "status": "ok"
}
🎧 Detect AI vs Human Voice (Base64 Input)
POST

/api/v1/detect
This endpoint accepts Base64 encoded audio input.

📥 Request Body
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "BASE64_ENCODED_AUDIO"
}
📤 Success Response
{
  "status": "success",
  "language": "Tamil",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.87,
  "explanation": "Low jitter and low shimmer indicate synthetic voice patterns"
}
❌ Error Response
{
  "status": "error",
  "message": "Invalid API key"
}
🧪 Testing the API
✅ Step 1: Run API Test Script
Start the server first:

uvicorn app.main:app --host 0.0.0.0 --port 8000
Then run:

python app/test_api.py
✅ Step 2: Run Client Test Script
python test_client.py
This behaves like an external user/client.

📌 Example Curl Request
curl -X POST "http://127.0.0.1:8000/api/v1/detect" \
-H "Content-Type: application/json" \
-H "x-api-key: your_api_key_here" \
-d '{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "BASE64_ENCODED_AUDIO"
}'
🐳 Docker Deployment
Build Docker Image
docker build -t dhvanisense .
Run Docker Container
docker run -p 8000:8000 dhvanisense
Now open:

http://127.0.0.1:8000/docs
☁️ Cloud Deployment
DhvaniSense can be deployed on:

Google Cloud Run

Google Compute Engine VM

Azure VM

AWS EC2

After deployment, your API endpoint will look like:

http://<public-ip>/api/v1/detect
📊 Output Files Generated
After running the full pipeline, these outputs will exist:

models/final_voice_model/ → Final trained model

models/checkpoints/ → Training checkpoints

models/config.json → Model configuration file

validation_results.csv → Validation results

🛠️ Common Errors & Fixes
❌ Error: FFmpeg not found / mp3 not loading
✅ Fix: Install FFmpeg and ensure it is in PATH.

Check:

ffmpeg -version
❌ Error: Model not found
This happens if you did not train the model.

✅ Fix:

python scripts/train_mini.py
❌ Error: Dataset missing
Ensure folder structure is correct:

data/ai/
data/human/
❌ Error: Uvicorn not installed
Install it:

pip install uvicorn
🧠 Tech Stack
Python

FastAPI

Uvicorn

NumPy

Pandas

Librosa (Audio Feature Extraction)

Scikit-learn / Deep Learning (based on your model)

FFmpeg (MP3 decoding)

Docker

🏆 Use Cases
Deepfake voice detection

Voice authenticity verification

AI voice fraud detection

Hackathon security solutions

Audio classification research

👨‍💻 Author
Developed by Sushanth Bandari
Project Name: DhvaniSense

📜 License
This project is intended for educational and hackathon purposes.
You may add an MIT / Apache license depending on your requirement.

⭐ Future Improvements
Add frontend UI for audio upload and detection

Improve dataset scaling and augmentation

Add GPU inference support

Add database logging for API requests

Add HTTPS + Domain integration for production deployment

Add support for more languages (Hindi, Telugu, Kannada, etc.)

✅ Final Note
Run the pipeline in order:

✅ Paths → Data Check → Train → Validate → Report → Run API → Test API

Then DhvaniSense will work smoothly 🚀

