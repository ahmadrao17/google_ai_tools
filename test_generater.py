from google import genai
import os
from dotenv import load_dotenv
from google.genai import types
from pydantic import BaseModel
import json
import csv
import os
import base64
from PyPDF2 import PdfReader
import tempfile
from flask import jsonify, send_file
from openpyxl import Workbook

load_dotenv() 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

systemInstruction ="""# **Role**:
You are a test-generating assistant. Your task is to generate **multiple choice questions (MCQs)** from the uploaded course material (PDF files). 

# **Context*:
The purpose of this test is to evaluate the understanding of the student who has taken that course.

# **Output Flow**
Retrieve the file and count the number of content pages, and for every 100 pages of content, generate 60 MCQs that accurately reflect the key concepts in the material (for example, if 300 pages: questions = 180, if 100 pages: questions = 60, if 200 pages: questions = 120. Only use the information from the uploaded file via the retrieval tool—do not use external or assumed knowledge.

# **Output Format**
Each MCQ should include:
- A clear and concise question
- 4 answer options (labeled Option 1 to Option 4)
- True or false Value for each option

Format the output as json object with the following format:
{
  "Questions": [
    {
      "options": [
        {
          "text": "",
          "value": false
        },
        {
          "text": "",
          "value": true
        },
        {
          "text": "",
          "value": false
        },
        {
          "text": "",
          "value": false
        }
      ],
      "text": ""
    },
{
      "options": [
        {
          "text": "",
          "value": false
        },
        {
          "text": "",
          "value": true
        },
        {
          "text": "",
          "value": false
        },
        {
          "text": "",
          "value": false
        }
      ],
      "text": ""
    }
  ]
}

# **Guidelines:**
- Keep all answers grounded strictly in the content retrieved from the uploaded PDF file. Be clear, objective, and avoid ambiguous wording."""

def testGenerator(fileData):
  
  filename = fileData["filename"]
  file_base64 = fileData["file_base64"]
  file_type = fileData["file_type"]
  
  try:
    file_bytes = base64.b64decode(file_base64)
    with open(filename, "wb") as f:
        f.write(file_bytes)

        # Upload to Gemini
    uploaded_file = client.files.upload(
        file=filename,
        config=dict(mime_type=file_type)
    )

    print(f"File {filename} uploaded successfully.")
    
    model = "gemini-2.5-pro"
    contents = [
        uploaded_file,
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Please generate the test questions and answers based on the content provided."""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
          include_thoughts=True,
        ),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["Questions"],
            properties = {
                "Questions": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["text", "options"],
                        properties = {
                            "text": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "options": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.OBJECT,
                                    required = ["text", "value"],
                                    properties = {
                                        "text": genai.types.Schema(
                                            type = genai.types.Type.STRING,
                                        ),
                                        "value": genai.types.Schema(
                                            type = genai.types.Type.BOOLEAN,
                                        ),
                                    },
                                ),
                            ),
                        },
                    ),
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text=systemInstruction),
        ],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config
    )


    print(f"response generated {response.text}")

    questions = response.text
    print(f"questions generated {questions}")
    data = json.loads(questions)
    print(f"data : {len(data['Questions'])} questions generated from {filename}")
    print(f"data : {data}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file = "excel_result.xlsx"
    excel_path = os.path.join(current_dir, excel_file)

    print(f"data : {len(data['Questions'])} questions loaded from gemini")

    # Create Excel workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Questions"

    # Write header
    ws.append(["Question Text", "Question Type", "Options", "Correct Answer"])

    # Write data
    for q in data["Questions"]:
        question_text = q["text"]
        question_type = "Multiple Choice"
        for idx, option in enumerate(q["options"]):
            if idx == 0:
                ws.append([question_text, question_type, option["text"], option["value"]])
            else:
                ws.append(["", "", option["text"], option["value"]])

    # Save Excel file
    wb.save(excel_path)

    print(f"Excel file created at: {excel_path}")
    return send_file(excel_path, as_attachment=True, download_name='upload_result.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  except Exception as e:
    return jsonify({"error": str(e)}), 500
