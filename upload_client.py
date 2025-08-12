import base64
import json
import requests
import os

API_URL = "http://127.0.0.1:5003/test-generator"
pdf_path = "Advanced ChatGPT Prompt Engineering_Mindstream x HubSpot.pdf"  # Use your actual file path

# Encode to base64
with open(pdf_path, "rb") as file:
    encoded_pdf = base64.b64encode(file.read()).decode("utf-8")

payload = {
    "filename": os.path.basename(pdf_path),
    "file_base64": encoded_pdf,
    "file_type": "application/pdf"
}
# Send POST request
response = requests.post(API_URL, json=payload)

# Save returned CSV
if response.status_code == 200:
    csv_filename = "upload_result.xlsx"
    with open(csv_filename, "wb") as f:
        f.write(response.content)
    print(f"✅ CSV file saved as: {csv_filename}")
else:
    print(f"❌ Failed to upload: {response.status_code}")
    print(response.json())
