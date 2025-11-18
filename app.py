import streamlit as st
from src.extractor import extract_invoice_data
from src.utils import load_image_preview, ensure_env_key
import pandas as pd
import json

st.set_page_config(
    page_title="Invoice Extractor",
    layout="wide",
)

# --- Sidebar Settings ---
# Add logo at the top of the sidebar
st.sidebar.image("assets/logo.png", use_container_width=True)
st.sidebar.title("Settings")
model_choice = st.sidebar.selectbox(
    "AI Model", ["gpt-4o-mini", "gpt-4o"], index=0
)

dpi = st.sidebar.slider("PDF Conversion DPI", 100, 300, 200)
show_raw = st.sidebar.checkbox("Show Raw Model Output", False)

# --- Main UI Layout ---
st.title("Invoice Extraction Tool")
st.write("Upload a PDF or image to extract structured invoice data.")

uploaded_file = st.file_uploader(
    "Upload invoice file", type=["pdf", "png", "jpg", "jpeg", "webp"]
)

col1, col2 = st.columns([1.3, 1])

if uploaded_file:
    # --- LEFT SIDE: PREVIEW ---
    with col1:
        st.subheader("Document Preview")
        previews = load_image_preview(uploaded_file)

        for idx, img in enumerate(previews):
            st.image(img, caption=f"Page {idx + 1}")

    # --- RIGHT SIDE: EXTRACTION ---
    with col2:
        st.subheader("Extracted Data")

        if st.button("Extract Invoice Data"):
            ensure_env_key()

            with st.spinner("Processing..."):
                result = extract_invoice_data(
                    uploaded_file,
                    model=model_choice,
                    pdf_dpi=dpi
                )

            if "error" in result:
                st.error(result["error"])
            else:
                # Display structured JSON
                st.json(result)

                # Convert to table-friendly dataframe
                df = pd.DataFrame([result])
                st.dataframe(df)

                # Download buttons
                st.download_button(
                    "Download JSON",
                    json.dumps(result, indent=2).encode("utf-8"),
                    "invoice.json",
                    "application/json"
                )

                st.download_button(
                    "Download CSV",
                    df.to_csv(index=False).encode("utf-8"),
                    "invoice.csv",
                    "text/csv"
                )

                if show_raw and "raw" in result:
                    st.subheader("Raw Model Output")
                    st.code(result["raw"])