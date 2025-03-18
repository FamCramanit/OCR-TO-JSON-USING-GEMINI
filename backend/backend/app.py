from flask import Flask, jsonify, request
from flask_cors import CORS  
from database import create_table  
from routes.history import history_bp  
import os
import fitz  # PyMuPDF ใช้แปลง PDF เป็นรูปภาพ
from PIL import Image  # ใช้จัดการไฟล์รูปภาพ
from helpers.image_processing import prep_image, extract_text_from_image
from helpers.text_parser import parse_extracted_text

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "../frontend/src/assets/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

def convert_pdf_to_jpg(pdf_path):
    """แปลง PDF เป็น JPG และคืนค่า path ของไฟล์ JPG"""
    doc = fitz.open(pdf_path)  # เปิดไฟล์ PDF
    jpg_paths = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()  # แปลงหน้า PDF เป็นภาพ
        img_path = pdf_path.replace(".pdf", f".jpg")  # ตั้งชื่อไฟล์ JPG
        pix.save(img_path)  # บันทึกภาพเป็นไฟล์ JPG
        jpg_paths.append(img_path)

    return jpg_paths  # คืนรายการไฟล์ JPG

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    file_ext = os.path.splitext(file.filename)[1].lower()  # ดึงนามสกุลไฟล์
    if file_ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Invalid file type. Only JPG, JPEG, PNG, and PDF (converted to images) are allowed."}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    if file_ext == ".pdf":
        try:
            file.save(file_path)  # บันทึกไฟล์ PDF ชั่วคราว
            jpg_paths = convert_pdf_to_jpg(file_path)  # แปลง PDF เป็น JPG
            os.remove(file_path)  # ลบไฟล์ PDF ต้นฉบับหลังแปลง

            if not jpg_paths:
                return jsonify({"error": "Failed to convert PDF to images"}), 500

            file_path = jpg_paths[0]  # ใช้รูปภาพจากหน้าแรกของ PDF
        except Exception as e:
            return jsonify({"error": f"PDF conversion failed: {str(e)}"}), 500
    else:
        file.save(file_path)  # บันทึกเฉพาะไฟล์รูปภาพ

    try:
        sample_file = prep_image(file_path)
        prompt = ("Extract the text in the image verbatim and identify: store name, Date(format: yyyy-mm-dd), Receipt number, items (format: Item name: quantity x price), vat (format: vat: number), total (format: total: number)")
        text = extract_text_from_image(sample_file, prompt)

        if text:
            structured_data = parse_extracted_text(text)
            return jsonify(structured_data), 200
        else:
            return jsonify({"error": "Failed to extract text from the image."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.register_blueprint(history_bp)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
