import base64
import os
import json
import re
from openai import OpenAI
from src.utils import file_to_images

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable.")
    return OpenAI(api_key=api_key)

def extract_json_from_text(text):
    """
    Extract JSON using regex and parse it safely.
    Handles extra text or markdown.
    """
    try:
        # Extract the first {...} block
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None, "No JSON object found in response."
        json_str = match.group(0)
        return json.loads(json_str), None
    except Exception as e:
        return None, f"JSON parsing error: {e}"

def call_vision_model(image_bytes_list, model="gpt-4o-mini"):
    client = get_openai_client()

    # System message to force JSON-only output
    messages = [{
        "role": "system",
        "content": (
            "You extract structured invoice data.\n"
            "You MUST respond with ONLY valid JSON.\n"
            "Do not add text, explanation, or comments outside JSON.\n"
            "If any fields are missing, return them as empty strings."
        )
    }]

    for img_bytes in image_bytes_list:
        b64 = base64.b64encode(img_bytes).decode("utf-8")
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract data from this invoice page."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]
        })

    # Request exact JSON schema
    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": """
Return strictly this JSON:

{
  "supplier": "",
  "supplier_address": "",
  "client": "",
  "client_address": "",
  "invoice_number": "",
  "invoice_date": "",
  "amount_ht": "",
  "amount_tva": "",
  "amount_ttc": "",
  "iban": "",
  "bic": "",
  "quality": ""
}
"""}
        ]
    })

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )

        raw_output = response.choices[0].message.content

        # Extract and parse JSON
        data, error = extract_json_from_text(raw_output)
        if error:
            return {"error": "Failed to parse JSON", "raw_output": raw_output, "parser_error": error}

        # Attach raw for debugging
        data["raw"] = raw_output
        return data

    except Exception as e:
        return {"error": str(e)}