# import os
import google.generativeai as genai

# ตั้งค่า API Key
API_KEY = ""
genai.configure(api_key=API_KEY)

# ฟังก์ชันอัปโหลดรูปภาพไปยัง Google Generative AI
def prep_image(image_path):
    sample_file = genai.upload_file(
        path=image_path, display_name="Receipt Image")
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
    return sample_file

# ฟังก์ชันดึงข้อความจากรูปภาพ
def extract_text_from_image(image_path, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([image_path, prompt])
    return response.text
