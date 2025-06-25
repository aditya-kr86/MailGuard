import streamlit as st
import joblib
import fitz  # PyMuPDF for PDF handling
import docx2txt
import re
import os
BASE_DIR = os.path.dirname(__file__)
tfidf = joblib.load(os.path.join(BASE_DIR, "tfidf.pkl"))
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))

# List of suspicious keywords for rule-based detection
suspicious_keywords = [
    "urgent", "verify", "click here", "congratulations", "free", "winner",
    "claim", "prize", "offer", "loan", "gift card", "bank", "account",
    "suspended", "password", "lottery", "scam", "refund", "reward",
    "upi", "kyc", "deposit", "selected", "lucky draw", "cash prize", "limited time"
]

# -------------------- Text Utilities --------------------

def preprocess(text):
    """Lowercase, remove digits and non-alphanumeric characters."""
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\W+', ' ', text)
    return text.strip()

def extract_text_from_pdf(file):
    """Extracts all text from uploaded PDF."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(file):
    """Extracts all text from uploaded DOCX."""
    return docx2txt.process(file)

def check_suspicious(text):
    """Returns a list of matched suspicious keywords from text."""
    text_lower = text.lower()
    return [kw for kw in suspicious_keywords if kw in text_lower]

# -------------------- Prediction Logic --------------------

def predict_spam(text, threshold=0.35):  # previously 0.2
    """Predict using ML model + rule-based flags."""
    cleaned = preprocess(text)
    vec = tfidf.transform([cleaned])
    prob = model.predict_proba(vec)[0][1]
    suspicious_flag = any(kw in text.lower() for kw in suspicious_keywords)

    if prob > threshold and suspicious_flag:
        label = "Spam/Scam"
    elif suspicious_flag:
        label = "Possibly Suspicious (Review)"
    elif prob > threshold:
        label = "Uncertain: High ML Score"
    else:
        label = "Not Spam"

    return label, prob, suspicious_flag


# -------------------- Streamlit App --------------------

def main():
    st.set_page_config(page_title="EmailGuard - Spam/Scam Detector", page_icon="🛡️")
    st.title("🛡️ EmailGuard: Multi-Input Spam & Scam Detector")

    st.write("Check if a message or document is spam, scam, or clean by using text input, file upload, or both.")

    # --- User Message Input ---
    user_message = st.text_area("📝 Enter your message here:")

    # --- File Upload (PDF, DOCX, TXT) ---
    uploaded_file = st.file_uploader("📄 Upload a document (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])

    combined_text = ""

    if uploaded_file:
        file_type = uploaded_file.type
        try:
            if file_type == "application/pdf":
                extracted = extract_text_from_pdf(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                extracted = extract_text_from_docx(uploaded_file)
            elif file_type == "text/plain":
                extracted = str(uploaded_file.read(), 'utf-8')
            else:
                st.error("❌ Unsupported file type. Please upload PDF, DOCX, or TXT.")
                return

            st.subheader("📃 Extracted Text from Document:")
            st.code(extracted[:1500] + ("..." if len(extracted) > 1500 else ""), language="text")
            combined_text += extracted

        except Exception as e:
            st.error(f"❌ Error processing the file: {e}")
            return

    # Combine text from both input + file
    if user_message.strip():
        combined_text += "\n" + user_message

    if not combined_text.strip():
        st.info("💡 Please enter a message or upload a document to analyze.")
        return

    # --- Prediction ---
    label, prob, suspicious = predict_spam(combined_text)
    suspicious_hits = check_suspicious(combined_text)

    st.subheader("📊 Result Summary")
    st.markdown(f"**Prediction:** `{label}`")
    st.markdown(f"**Spam Probability:** `{prob:.2f}`")

    # --- Alerts ---
    if label == "Spam/Scam":
        st.error("🚨 This message is classified as Spam or Scam.")
        if prob < 0.3:
            st.caption("🧠 ML model shows low probability, but rule-based system flagged scam patterns.")

    elif label == "Possibly Suspicious (Review)":
        st.warning("⚠️ Rule-based check flagged this message. Review with caution.")

    else:
        st.success("✅ No suspicious patterns or scam detected.")

    if suspicious_hits:
        st.markdown(f"🔍 Suspicious keywords detected: `{', '.join(suspicious_hits)}`")

# Run the app
if __name__ == "__main__":
    main()
