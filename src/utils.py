import fitz  # PyMuPDF
from PIL import Image
import io
from dotenv import load_dotenv
import json
import os

def ensure_env_key():
    """
    Ensure OPENAI_API_KEY is available.
    """
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("You must set OPENAI_API_KEY in your environment.")


def convert_pdf_to_images(pdf_bytes, dpi=180):
    """
    Convert PDF pages to JPEG bytes.
    """
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []

    for page in pdf:
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        images.append(buffer.getvalue())

    return images


def load_image_preview(file):
    file_bytes = file.read()
    file.seek(0)

    if file.type == "application/pdf":
        pages = convert_pdf_to_images(file_bytes)
        return [Image.open(io.BytesIO(pg)) for pg in pages]

    else:
        return [Image.open(io.BytesIO(file_bytes))]


def file_to_images(file, dpi=180):
    """
    Always return a list of JPEG bytes for model input.
    Handles both PDFs and images safely.
    """
    file_bytes = file.read()
    file.seek(0)  # reset stream pointer

    if file.type == "application/pdf":
        return convert_pdf_to_images(file_bytes, dpi=dpi)

    else:
        img = Image.open(io.BytesIO(file_bytes))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        return [buffer.getvalue()]


def safe_json_load(text):
    """
    Load model output safely into JSON.
    """
    try:
        return json.loads(text)
    except Exception:
        return None