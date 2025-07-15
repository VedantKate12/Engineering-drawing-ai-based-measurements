# app.py

import streamlit as st
from PIL import Image
from drawing_utils import process_drawing_streamlit
import base64
st.set_page_config(page_title="Engineering Drawing Extractor", layout="centered")

st.title("📐 Engineering Drawing Dimension Extractor")

uploaded_file = st.file_uploader("Upload an Engineering Drawing", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Drawing", use_column_width=True)

    if st.button("🧠 Process Drawing"):
        with st.spinner("Processing..."):
            annotated_img_path, summary, objects, pdf_path = process_drawing_streamlit(img)

        st.image(annotated_img_path, caption="Detected Components", use_column_width=True)

        st.markdown("### 📄 Summary")
        st.write(summary)

        st.markdown("### 🧾 Component Table")
        for obj in objects:
            st.write(f"{obj['label']} | Length: {obj['length_mm']:.2f} mm | BBox: {obj['bbox']}")

        with open(pdf_path, "rb") as f:
            b64_pdf = base64.b64encode(f.read()).decode("utf-8")
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="drawing_report.pdf">📥 Download PDF Report</a>'
            st.markdown(href, unsafe_allow_html=True)