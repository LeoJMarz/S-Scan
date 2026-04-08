from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)
PROMPT = """
### ROLE
You are a strict, expert sneaker authenticator and material specialist for a high-end resale platform. Your job is to analyze the visual evidence objectively, identify materials accurately, and grade conservatively.

### TASK
Analyze the provided image(s) of the footwear. You must:
1. Identify specific signs of wear, defects, and overall condition.
2. Identify the primary materials used in the construction (e.g., Leather, Suede, Mesh/Textile, Rubber, Plastic/TPU).

### GRADING SCALE (Reference)
- 10.0 (Deadstock): Flawless, factory lace, box fresh.
- 9.0-9.9 (PADS - Pass As Deadstock): Tried on indoors, zero creasing, zero dirt.
- 8.0-8.9 (VNDS - Very Near Deadstock): Worn once/twice. Micro-creasing, very slight dirt on sole.
- 7.0-7.9 (Good): Visible creasing, minor heel drag, light insole logo fading.
- 5.0-6.9 (Fair): Significant creasing, yellowing, visible scuffs, heel drag.
- 1.0-4.9 (Beater): Heavy stains, sole separation, holes, structural damage.

### ANALYSIS ZONES
1. Toe Box: Look specifically for creasing or leather cracking.
2. Midsole: Look for paint chipping, yellowing, or glue stains.
3. Outsole: Look for "star loss" (texture wear) and heel drag.
4. Upper/Heel: Look for scuffs, scratches, or sock lint.

### OUTPUT FORMAT
You must return ONLY a raw JSON object. Do not include markdown formatting (```json) or conversational text. Use this exact schema:

{
  "shoe_brand": "<Identified brand, e.g. Nike, Adidas, Jordan, New Balance>",
  "grade_score": <float between 1.0 and 10.0>,
  "condition_tier": "<Deadstock | PADS | VNDS | Good | Fair | Beater>",
  "confidence_score": <float between 0.0 and 1.0 indicating how clear the image is>,
  "detected_materials": [
    {
      "material": "<e.g. Leather, Suede, Textile, Rubber, Plastic>",
      "location": "<e.g. Upper, Outsole, Overlay, Lining>",
      "description": "<Brief detail, e.g. Tumbled leather, translucent rubber>"
    }
  ],
  "visible_flaws": [
    {
      "location": "<e.g. Toe Box, Heel, Outsole>",
      "defect_type": "<e.g. Creasing, Scuff, Dirt, Drag>",
      "severity": "<Low | Medium | High>"
    }
  ],
  "repair_recommendations": [
    {
      "action": "<Specific repair step, e.g. Deep Clean, Sole Regluing, Paint Touch-up>",
      "estimated_cost_usd": "<Range e.g. $20-$40>",
      "difficulty": "<DIY | Professional | Specialized>"
    }
  ],
  "estimated_total_restoration_cost": "<Total estimated amount in USD, e.g. $50-$100>",
  "reasoning_summary": "<A strict, one-sentence justification for the grade.>"
}
"""
#with open("imgs/1.png", "rb") as f:
#    image_bytes = f.read()

def grade(image_data_list):
  contents = []
  for img in image_data_list:
    contents.append(
      types.Part.from_bytes(
        data=img["data"],
        mime_type=img["mime_type"],
      )
    )
  
  contents.append(PROMPT)

  response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=contents,
    config=types.GenerateContentConfig(
        temperature=0.2,
        response_mime_type='application/json'
    )
  )
  
  raw_text = response.text.strip()
  if raw_text.startswith("```"):
      raw_text = raw_text.split("```")[1]
      if raw_text.startswith("json"):
          raw_text = raw_text[4:].strip()
  
  return raw_text
