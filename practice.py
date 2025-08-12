import json
import csv
import os

# # Get the current script's directory
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Define the JSON file name
# json_file = 'openai.json'  # replace with your actual file name
# csv_file = 'output.csv'

# # File paths
# json_path = os.path.join(current_dir, json_file)
# csv_path = os.path.join(current_dir, csv_file)

# # Load JSON
# with open(json_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# print(f"data : {len(data['Questions'])} questions loaded from {json_file}")

# with open(csv_path, mode="w", newline='', encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Question Text", "Question Type", "Options", "Correct Answer"])
    
#     for q in data["Questions"]:
#         question_text = q["text"]
#         question_type = "Multiple Choice"
#         for option in q["options"]:
#             if q["options"].index(option) == 0:
#                 writer.writerow([question_text, question_type, option["text"], option["value"]])
#             else:
#                 question_text = ""
#                 question_type = ""
#                 writer.writerow([question_text, question_type, option["text"], option["value"]])    

# print(f"CSV created at: {csv_path}")


jsonData = """
{
  "Questions": [
    {
      "text": "According to the Sunni perspective presented in the text, why was Hazrat Ali (RA) absent from the Saqifah meeting?",
      "options": [
        {
          "text": "He was in political opposition to the gathering and chose not to attend.",
          "value": false
        },
        {
          "text": "He prioritized the Prophet's (PBUH) ritual washing and burial over political matters.",
          "value": true
        },
        {
          "text": "He was gathering his own supporters to make a bid for the caliphate.",
          "value": false
        },
        {
          "text": "He was unaware that the meeting to select the next leader was taking place.",
          "value": false
        }
      ]
    },
    {
      "text": "What does the Sunni tradition, as mentioned in the document, attribute the delay in Hazrat Ali's (RA) pledge of allegiance to Abu Bakr (RA) to?",
      "options": [
        {
          "text": "A political protest against the legitimacy of Abu Bakr's (RA) appointment.",
          "value": false
        },
        {
          "text": "A desire to negotiate a more powerful position within the new leadership.",
          "value": false
        },
        {
          "text": "Personal grief and the sorrow of Fatimah (RA) following the Prophet's (PBUH) death.",
          "value": true
        },
        {
          "text": "A disagreement over the policies established during the Saqifah meeting.",
          "value": false
        }
      ]
    },
    {
      "text": "How did Hazrat Ali (RA) contribute to Abu Bakr's (RA) caliphate according to the text?",
      "options": [
        {
          "text": "He publicly opposed Abu Bakr's leadership and led a faction against him.",
          "value": false
        },
        {
          "text": "He completely withdrew from public life and refused to participate in state affairs.",
          "value": false
        },
        {
          "text": "He offered moral support, refrained from divisive actions, and participated in advisory councils.",
          "value": true
        },
        {
          "text": "He only participated in military campaigns and avoided political matters.",
          "value": false
        }
      ]
    }
  ]
}"""


# Convert JSON string to Python dictionary
print(type(jsonData))
data = json.loads(jsonData)

# Now `data` is a dictionary, and you can use it like:
print(data["Questions"][0]["text"])
print(data["Questions"][0]["options"][1]["value"])