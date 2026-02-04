import base64
import requests

API_URL = "http://127.0.0.1:8000/detect"
HEADERS = {"x-api-key": "sk_test_123456789"}

def test_file(file_path, lang="Tamil"):
    # 1. Read MP3 and encode to Base64
    with open(file_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")

    # 2. Construct JSON payload
    payload = {
        "language": lang,
        "audioFormat": "mp3",
        "audioBase64": encoded_string
    }

    # 3. Post to API
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    print(response.json())

if __name__ == "__main__":
    test_file("path/to/your/sample.mp3")