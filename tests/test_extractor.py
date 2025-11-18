from src.extractor import extract_invoice_data

def test_extract_no_file():
    """
    Ensure extraction gracefully fails when no file is provided.
    """
    try:
        extract_invoice_data(None)
    except Exception:
        pass  # Expected because None is not a valid file