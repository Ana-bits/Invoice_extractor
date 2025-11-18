from src.models import call_vision_model
from src.utils import file_to_images
import json

def extract_invoice_data(file, model="gpt-4o-mini", pdf_dpi=180):
    """
    Full pipeline: file -> images -> AI model -> JSON -> return structured dict
    """
    try:
        images = file_to_images(file, dpi=pdf_dpi)
        result = call_vision_model(images, model=model)

        # If model returned an error dict
        if isinstance(result, dict) and "error" in result:
            return {
                "error": result["error"],
                "raw_output": result.get("raw_output") if isinstance(result, dict) else None,
                "parser_error": result.get("parser_error") if isinstance(result, dict) else None
            }

        # If result is a string, try parsing
        if isinstance(result, str):
            try:
                json_data = json.loads(result)
            except Exception:
                return {
                    "error": "Failed to parse JSON.",
                    "raw_output": result
                }
        else:
            # result is already dict
            json_data = result

        # Attach raw output safely
        if "raw" not in json_data:
            json_data["raw"] = result if isinstance(result, str) else None

        return json_data

    except Exception as e:
        return {"error": str(e)}
