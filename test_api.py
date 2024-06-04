import requests
import logging
import os

# Set up the environment for Tesseract-OCR
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def get_text_from_api(image_path):
    url = 'http://localhost:5000/get-text'
    try:
        with open(image_path, 'rb') as img:
            files = {'image': img}
            response = requests.post(url, files=files)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response from /get-text: {data}")
            return data
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred in get_text_from_api: {e}")

def get_bboxes_from_api(image_path):
    url = 'http://localhost:5000/get-bboxes'
    try:
        with open(image_path, 'rb') as img:
            files = {'image': img}
            response = requests.post(url, files=files)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response from /get-bboxes: {data}")
            return data
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred in get_bboxes_from_api: {e}")

if __name__ == "__main__":
    image_path = 'C:/Users/Admin/Desktop/OCR API/img.png'
    text_data = get_text_from_api(image_path)
    bboxes_data = get_bboxes_from_api(image_path)

    if text_data:
        print(f"OCR Text: {text_data.get('text')}")

    if bboxes_data:
        print(f"Bounding Boxes: {bboxes_data.get('bboxes')}")