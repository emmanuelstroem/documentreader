from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import requests, json, io, os
import PyPDF2
from PIL import PngImagePlugin, PdfImagePlugin, Image

# Create your views here.
def document(self, id):
  # fetch and return document
  return fetch_document(id)

def health_check(self):
  health_status = {
        'status' : 'Healthy'
    }
  return HttpResponse(json.dumps(health_status), content_type='application/json')


# Fetch PDF or PNG
def fetch_document(with_id):
  # Handle HTTP Request exceptions
  try:
    response = requests.get(generate_url(id))
    content_type = response.headers['Content-Type']
    if is_valid_document(response, content_type):
      return respond_with(response, content_type, error=False)
    else:
      return respond_with("Invalid .{} Document", content_type, error=True)
  except requests.exceptions.HTTPError as http_error:
    return respond_with("HTTP Request Error: {}", http_error, error=True)
  except requests.exceptions.InvalidURL as invalid_url:
    return respond_with("Invalid URL Error: {}", invalid_url, error=True)
  except requests.exceptions.Timeout as timeout_error:
    return respond_with("HTTP Request Timeout Error: {}", timeout_error, error=True)
  #  Add additional Request.get exceptions here

# Generate Request URL
def generate_url(with_id):
  base_url = os.getenv('BASE_URL', 'http://localhost:3000')
  url = "{}/{}".format(base_url, with_id)
  return url

# Check if Document is Valid
def is_valid_document(response, content_type):
  doc_type = content_type.split('/')[1]

  # Check PDF handling exceptions
  if doc_type == 'pdf':
    try:
      with io.BytesIO(response.content) as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        return True if read_pdf else False
    except PyPDF2.utils.PdfReadError as pdf_read_error:
      return False
    except PyPDF2.utils.PyPdfError as pdf_error:
      print(pdf_error)
      return False
    # Add additional PyPDF2 excetions here
  # Check PNG handling exceptions
  elif doc_type == 'png':
    try:
      image_file =  Image.open(io.BytesIO(response.content))
      return True if PngImagePlugin.PngImageFile.verify(image_file) is None else False
    except OSError as os_error:
        print(os_error)
    # Add additional PngImagePlugin excetions here
  # Undefined Document Type
  else:
    return respond_with("Unknown Document Type: {}", doc_type, error=True)

# Response to Browser
def respond_with(response, content_type, error):
  # check if error
  if error:
    message = response.format(content_type.split('/')[1])
    error = {
        'error' : message
    }
    return HttpResponse(json.dumps(error), content_type='application/json')
  else:
    return HttpResponse(response, content_type=content_type)
