# drawing_utils.py

from ultralytics import YOLO
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from fpdf import FPDF
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO)

model = YOLO("yolov8n.pt")  

class DrawingReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Engineering Drawing Report", ln=True, align="C")

    def add_image(self, img_path):
        self.image(img_path, x=10, y=30, w=180)
        self.ln(85)

    def add_table(self, objects):
        self.set_font("Arial", "", 12)
        self.cell(0, 10, "Detected Components:", ln=True)
        self.set_font("Arial", "", 10)
        for obj in objects:
            text = f"{obj['label']} at {obj['bbox']} - Est. Length: {obj['length_mm']:.2f} mm"
            self.cell(0, 10, text, ln=True)

    def add_summary(self, summary):
        self.ln(10)
        self.set_font("Arial", "I", 12)
        self.multi_cell(0, 10, summary)

def extract_scale_ratio(img):
    text = pytesseract.image_to_string(img)
    if "1:" in text:
        try:
            scale = int(text.split("1:")[1].split()[0])
            return 1 / scale
        except:
            return 0.01
    return 0.01

def estimate_length(pt1, pt2, pixel_per_mm):
    return cv2.norm(np.array(pt1) - np.array(pt2)) / pixel_per_mm

def process_drawing_streamlit(img):
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    results = model(img_cv)[0]

    scale_ratio = extract_scale_ratio(img_cv)
    pixel_per_mm = 10 / 100  # Dummy ratio

    objects = []
    label_counts = {}

    for box in results.boxes:
        xyxy = box.xyxy[0].cpu().numpy()
        label = model.names[int(box.cls[0])]
        pt1, pt2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
        length_mm = estimate_length(pt1, pt2, pixel_per_mm)
        objects.append({
            "label": label,
            "bbox": [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])],
            "length_mm": length_mm
        })
        label_counts[label] = label_counts.get(label, 0) + 1
        cv2.rectangle(img_cv, pt1, pt2, (0, 255, 0), 2)
        cv2.putText(img_cv, f"{label} ({length_mm:.1f} mm)", pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

    summary = "The drawing contains:\n"
    for label, count in label_counts.items():
        summary += f" - {count} {label}(s)\n"
    if objects:
        max_obj = max(objects, key=lambda x: x['length_mm'])
        summary += f"\nThe longest object is a {max_obj['label']} of length {max_obj['length_mm']:.2f} mm."

    # Save image
    annotated_path = "annotated_image.png"
    cv2.imwrite(annotated_path, img_cv)

    # Generate PDF
    pdf = DrawingReport()
    pdf.add_page()
    pdf.add_image(annotated_path)
    pdf.add_table(objects)
    pdf.add_summary(summary)
    pdf_path = "drawing_report.pdf"
    pdf.output(pdf_path)

    return annotated_path, summary, objects, pdf_path
