
# Engineering Drawing Dimension Extractor

This project extracts dimensions and classifies engineering components from technical drawings using deep learning and computer vision. It uses YOLOv8 for object detection and Tesseract OCR for reading scale labels from drawings to convert pixel distances into real-world measurements.

## Features

- Object Detection: Detects components such as shafts, holes, bolts, gears using YOLOv8.
- Scale Detection: Uses Tesseract OCR to detect scales like "1:100" or "10 mm".
- Real-world Length Estimation: Converts pixel lengths into millimeters using the detected scale.
- Annotated Output: Returns an annotated image with bounding boxes and measurements.
- PDF Report: Auto-generates a professional PDF report with image, tables, and summary.
- Natural Language Summary: Describes the drawing in a human-readable paragraph.
- Streamlit UI: Easy-to-use interface for uploading images and downloading reports.

## Tech Stack

- Python
- OpenCV
- YOLOv8 (Ultralytics)
- Pytesseract (Tesseract OCR)
- Streamlit
- FPDF
- Pillow (PIL)
- LabelImg (for custom annotations)

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Tesseract OCR (installed and configured)



```bash
git clone https://github.com/yourusername/drawing-extractor.git
cd drawing-extractor
1. Install Python Packages
bash
Copy
Edit
pip install ultralytics opencv-python pytesseract streamlit fpdf pillow
2. Install Tesseract OCR
Windows:
Download and install from:
https://github.com/UB-Mannheim/tesseract/wiki
Default path:
C:\Program Files\Tesseract-OCR\tesseract.exe

Add this to your drawing_utils.py:

python
Copy
Edit
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
3. Run the Streamlit App
bash
Copy
Edit
streamlit run app.py
4. Use the App
Upload an engineering drawing image

Click "Process Drawing"

View annotated image, object table, and summary

Download the PDF report
