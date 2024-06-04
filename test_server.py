import pytest
from server import app  # Import the Flask app from server.py
from io import BytesIO
from PIL import Image
import os

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def create_test_image():
    image_path = "C:/Users/Admin/Desktop/OCR API/img/img.png"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    # Create a simple image if it doesn't exist
    if not os.path.exists(image_path):
        img = Image.new('RGB', (100, 100), color='red')
        img.save(image_path)
    return image_path

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the OCR API" in response.data

def test_get_text_endpoint(client, create_test_image):
    image_path = create_test_image
    with open(image_path, "rb") as img:
        data = {'image': (BytesIO(img.read()), 'img.png')}
        response = client.post('/get-text', content_type='multipart/form-data', data=data)
        assert response.status_code == 200
        assert 'text' in response.get_json()

def test_get_bboxes_endpoint(client, create_test_image):
    image_path = create_test_image
    with open(image_path, "rb") as img:
        data = {'image': (BytesIO(img.read()), 'img.png')}
        response = client.post('/get-bboxes', content_type='multipart/form-data', data=data)
        assert response.status_code == 200
        assert 'bboxes' in response.get_json()

def test_get_text_no_image(client):
    response = client.post('/get-text', content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.get_json()
    assert response.get_json()['error'] == 'No image file in request'

def test_get_bboxes_no_image(client):
    response = client.post('/get-bboxes', content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.get_json()
    assert response.get_json()['error'] == 'No image file in request'

def test_get_text_invalid_image(client):
    data = {'image': (BytesIO(b'not an image'), 'test.txt')}
    response = client.post('/get-text', content_type='multipart/form-data', data=data)
    assert response.status_code == 500
    assert 'error' in response.get_json()

def test_get_bboxes_invalid_image(client):
    data = {'image': (BytesIO(b'not an image'), 'test.txt')}
    response = client.post('/get-bboxes', content_type='multipart/form-data', data=data)
    assert response.status_code == 500
    assert 'error' in response.get_json()

def test_get_text_exception(client, monkeypatch):
    def mock_image_to_string(image):
        raise Exception("Mocked exception")
    monkeypatch.setattr("pytesseract.image_to_string", mock_image_to_string)
    
    image_path = "C:/Users/Admin/Desktop/OCR API/img/img.png"
    with open(image_path, "rb") as img:
        data = {'image': (BytesIO(img.read()), 'img.png')}
        response = client.post('/get-text', content_type='multipart/form-data', data=data)
        assert response.status_code == 500
        assert 'error' in response.get_json()

def test_get_bboxes_exception(client, monkeypatch):
    def mock_image_to_data(image, output_type):
        raise Exception("Mocked exception")
    monkeypatch.setattr("pytesseract.image_to_data", mock_image_to_data)
    
    image_path = "C:/Users/Admin/Desktop/OCR API/img/img.png"
    with open(image_path, "rb") as img:
        data = {'image': (BytesIO(img.read()), 'img.png')}
        response = client.post('/get-bboxes', content_type='multipart/form-data', data=data)
        assert response.status_code == 500
        assert 'error' in response.get_json()