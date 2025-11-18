# Invoice Extractor AI

A professional AI-powered invoice extraction tool built in **Python + Streamlit**, capable of parsing **PDFs and images** (PNG, JPG, JPEG, WebP) to extract structured invoice data automatically using **OpenAI's GPT-4o vision model**.

---

## Features

* Upload PDF or image invoices.
* Multi-page PDF support.
* Extracts structured fields:

```json
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
  "quality": "",
  "raw": "..."   // raw GPT response for debugging
}
```

* Fully robust JSON parsing even if GPT returns extra text.
* Streamlit split-view UI for **uploaded invoice + extracted JSON side-by-side**.
* Handles PDFs and images in a single workflow.

---

## Installation

```bash
git clone https://github.com/yourusername/invoice-extractor-ai.git
cd invoice-extractor-ai
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

Install Python-dotenv to manage environment variables:

```bash
pip install python-dotenv
```

Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

---

## Run the App

```bash
streamlit run app.py
```

* Upload a PDF or image.
* Wait a few seconds for GPT-4o to process.
* View structured invoice JSON side-by-side with the uploaded file.

---

## Project Structure

```
invoice-extractor/
│
├── app.py                  # Streamlit main app
├── requirements.txt        # Python dependencies
├── README.md
│
├── src/
│   ├── extractor.py       # Pipeline combining file -> images -> GPT -> JSON output
│   ├── utils.py           # File-to-images & helper functions
│   └── models.py          # GPT-4o vision model integration
│
├── assets/                # Optional folder for example invoices, images,,,
│   ├── sample_invoice.pdf
│   ├── example_invoice.jpg
│   └── logo.png
│
├── tests/                 # Unit tests for utils and model calls
│   ├── test_extractor.py
│   └── test_utils.py
│
├── .env                   # Contains OPENAI_API_KEY
└── .gitignore
```

---

## Notes

* Designed for personal or internal use. Ensure you have the rights to process invoices.
* Tested with GPT-4o-mini for speed; GPT-4o can be used for higher quality but may be slower.
* Supports local image files and PDFs without uploading to external servers.
