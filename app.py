from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from openai import OpenAI
import logging
import os
from PIL import Image
import io
import base64
import requests
import json

# Configure logging
LOG_FILENAME = os.getenv('LOG_FILENAME', '/app/logs/app.log')
logging.basicConfig(level=logging.INFO, filename=LOG_FILENAME,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set OpenAI API key
api_key = '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'  # Replace with your OpenAI API key

client = OpenAI(api_key=api_key)

def convert_pdf_to_images(pdf_path):
    """
    Convert PDF pages to images.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        list: List of PIL Image objects.
    """
    doc = fitz.open(pdf_path)
    images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img_data = pix.tobytes("ppm")
        img = Image.open(io.BytesIO(img_data))
        images.append(img)
    
    return images
    
def image_to_base64(img):
    """
    Convert PIL image to base64 encoded string.
    
    Args:
        img (PIL.Image.Image): PIL Image object.
    
    Returns:
        str: Base64 encoded string of the image.
    """
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def extract_troubleshooting_info_from_image(images):
    """
    Extract troubleshooting information from images using OpenAI API.
    
    Args:
        images (list): List of PIL Image objects.
    
    Returns:
        str: JSON formatted troubleshooting information.
    """
    Instructions = '''
        It's a product user manual.
        Locate the page number of "trouble shooting" part and extract trouble shooting information in related page.
        Return contents in JSON format without any other words. Show me the original words.
        The response structure in each page must be in page->troubleshooting->...
    '''
    
    content = [{"type": "text", "text": Instructions.strip()}]
    for img in images:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_to_base64(img)}"
            },
        })
        
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ]
    )
    
    return response.choices[0].message.content

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """
    Handle PDF file upload and return extracted troubleshooting information.
    
    Returns:
        response (flask.Response): JSON response containing troubleshooting information or error message.
    """
    logger.info("Received a file upload request")
    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({"status": "error", "message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({"status": "error", "message": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        file_path = f"/tmp/{file.filename}"
        file.save(file_path)
        logger.info(f"File saved to {file_path}")

        # Convert PDF to images
        images = convert_pdf_to_images(file_path)
        troubleshooting_info = extract_troubleshooting_info_from_image(images).split('```json\n')[-1].split('\n```')[0]
        
        logger.info(f"Successfully extracted troubleshooting information: {troubleshooting_info}")
        return jsonify({"status": "success", "troubleshooting_info": troubleshooting_info}), 200

    logger.error("Invalid file format")
    return jsonify({"status": "error", "message": "Invalid file format"}), 400

if __name__ == '__main__':
    logger.info("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)
