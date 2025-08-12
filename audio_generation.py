# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import mimetypes
import os
import re
import struct
from google import genai
from google.genai import types
from dotenv import load_dotenv
import wave



load_dotenv() 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


def generate():
    
    
    uploaded_file = client.files.upload(
        file="Advanced ChatGPT Prompt Engineering_Mindstream x HubSpot.pdf" ,
        config=dict(mime_type="application/pdf")
    )

    model = "gemini-2.5-pro-preview-tts"
    contents = [
        uploaded_file,
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Please convert the uploaded PDF file into an audio file."""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
               voice_name='Kore',
            )
         )
      ),
    )
    response = client.models.generate_content(
    model=model,
    contents=contents,
    config=generate_content_config,
    )
    data = response.candidates[0].content.parts[0].inline_data.data

    file_name='out.wav'
    wave_file(file_name, data) # Saves the file to current directory

def wave_file(file_name, data):
    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit samples
        wf.setframerate(24000)  # Sample rate
        wf.writeframes(data)
    print(f"Audio file saved to: {file_name}")


if __name__ == "__main__":
    generate()
