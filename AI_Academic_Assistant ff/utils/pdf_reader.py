import fitz  # PyMuPDF


def extract_text(uploaded_file):
    """
    Extract text from Streamlit uploaded PDF.
    """

    if uploaded_file is None:
        return ""

    text = ""

    try:
        if isinstance(uploaded_file, str):
            # Open direct file path
            document = fitz.open(uploaded_file)
        else:
            # Read uploaded file
            pdf_bytes = uploaded_file.read()

            # Open PDF
            document = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

        # Read every page
        for page in document:
            page_text = page.get_text("text")

            if page_text:
                text += page_text + "\n"

        document.close()

        return text.strip()

    except Exception as e:
        return f"Error reading PDF: {str(e)}"