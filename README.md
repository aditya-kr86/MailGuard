# EmailGuard: Multi-Input Spam & Scam Detector

## Overview

**EmailGuard** (in `app.py`) is a Streamlit-based web application for detecting spam and scam content in user messages and uploaded documents. It leverages a machine learning (ML) model alongside rule-based keyword checks to assess whether a message or document is likely to be spam, scam, or clean.

- **Multi-Input:** Analyze plain text, PDF, DOCX, or TXT files—or a combination.
- **Hybrid Detection:** Uses both ML and a list of suspicious keywords for robust analysis.
- **User-Friendly:** Provides clear, actionable results and warnings.

---

## Features

- **Text & Document Input:**  
  Users can type a message, upload a document, or both. Supported document types:
  - PDF (`.pdf`)
  - Word (`.docx`)
  - Plain text (`.txt`)

- **Spam/Scam Detection:**  
  Combines ML prediction and rule-based keyword matching for improved accuracy.

- **Transparent Output:**  
  Shows prediction label, probability score, and highlights detected suspicious keywords.

- **Streamlit UI:**  
  Simple, interactive interface with clear visual cues (success, warning, error alerts).

---

## How It Works

1. **Input:**  
   - User enters text and/or uploads a document.
   - Supported file types: PDF, DOCX, TXT.

2. **Text Extraction & Preprocessing:**  
   - Extracts all text from uploaded files.
   - Preprocesses content (lowercasing, removing digits/non-alphanumerics).

3. **Spam/Scam Analysis:**  
   - **ML Model:** Calculates probability of spam/scam.
   - **Rule-Based:** Checks for presence of known suspicious keywords.

4. **Result Display:**  
   - Shows prediction label (Spam/Scam, Possibly Suspicious, Uncertain, Not Spam).
   - Displays probability score.
   - Lists matched suspicious keywords (if any).
   - Visual alerts for dangerous content.

---

## Setup & Usage

### Requirements

- Python 3.7+
- `streamlit`
- `joblib`
- `PyMuPDF` (`fitz`)
- `docx2txt`
- Trained ML model files: `tfidf.pkl`, `model.pkl` (must be present in the same directory as `app.py`)

### Installation

```bash
pip install streamlit joblib pymupdf docx2txt
```

### Running the App

```bash
streamlit run app.py
```

- Make sure `tfidf.pkl` and `model.pkl` are present in the same directory as `app.py`.
- Access the app at `http://localhost:8501` in your browser.

---

## File Structure

```
app.py           # Main Streamlit app
tfidf.pkl        # TF-IDF vectorizer (required)
model.pkl        # Trained ML model (required)
README.md        # This file
```

---

## Key Functions

- `preprocess(text)`: Cleans and normalizes input text.
- `extract_text_from_pdf(file)`: Extracts text from PDF files.
- `extract_text_from_docx(file)`: Extracts text from DOCX files.
- `check_suspicious(text)`: Returns list of matched suspicious keywords.
- `predict_spam(text, threshold)`: Combines ML and rule-based logic to predict spam/scam.

---

## Customization

- **Suspicious Keywords:**  
  Edit or expand the `suspicious_keywords` list in `app.py` to cover more scam/phishing patterns.

- **Model Threshold:**  
  Adjust the `threshold` parameter in `predict_spam` for stricter or more lenient spam detection.

---

## Disclaimer

- The effectiveness of detection depends on the quality of the trained ML model (`model.pkl`) and the comprehensiveness of the `suspicious_keywords` list.
- Always review flagged messages manually for maximum security.

---

## License

[MIT License](LICENSE)  
© 2025 [@aditya-kr86](https://github.com/aditya-kr86)

---
