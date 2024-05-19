from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def extract_troubleshooting_info(pdf_path):
    doc = fitz.open(pdf_path)
    troubleshooting_info = []
    
    # Logic to extract troubleshooting sections from specific pages
    # Assuming troubleshooting sections are always on specific pages as per the task.
    pages_to_check = [8, 31, 32]  # Page indices start at 0

    for page_num in pages_to_check:
        if page_num < len(doc):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if "troubleshooting" in text.lower():
                troubleshooting_info.append({
                    "page": page_num + 1,  # Human-readable page number
                    "text": text.strip()
                })
    return troubleshooting_info

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.pdf'):
        file_path = f"/tmp/{file.filename}"
        file.save(file_path)

        troubleshooting_info = extract_troubleshooting_info(file_path)
        return jsonify(troubleshooting_info), 200

    return "Invalid file format", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
