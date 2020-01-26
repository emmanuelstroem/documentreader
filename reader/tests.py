from django.test import TestCase
from . import views
import requests

# Create your tests here.
class ReaderViewsTest(TestCase):
  def test_url(self):
    expected_url = "http://localhost:3000/10"
    tenth_doc_url = views.generate_url(10)
    self.assertEquals(expected_url, tenth_doc_url)

  def test_is_valid_pdf_document(self):
    response = requests.get('https://github.com/e-conomic/hiring-assigments/raw/master/sre/dummy-pdf-or-png/dummy.pdf')
    content_type = 'application/pdf'  #hard coded content type because Github responds with application/octet-stream
    is_valid = views.is_valid_document(response, content_type)
    self.assertTrue(is_valid)

  def test_is_not_valid_pdf_document(self):
    response = requests.get('https://github.com/e-conomic/hiring-assigments/raw/master/sre/dummy-pdf-or-png/corrupt-dummy.pdf')
    content_type = 'application/pdf' #hard coded content type because Github responds with application/octet-stream
    is_valid = views.is_valid_document(response, content_type)
    self.assertFalse(is_valid)

  def test_is_valid_png_document(self):
    response = requests.get('https://github.com/e-conomic/hiring-assigments/raw/master/sre/dummy-pdf-or-png/dummy.png')
    content_type = 'application/png'  #hard coded content type because Github responds with application/octet-stream
    is_valid = views.is_valid_document(response, content_type)
    self.assertTrue(is_valid)

  def test_different_document_type(self):
    response = requests.get('https://github.com/e-conomic/hiring-assigments/raw/master/sre/dummy-pdf-or-png/dummy.png')
    content_type = 'application/pdf'  #hard coded content type because Github responds with application/octet-stream
    same_content_type = views.is_valid_document(response, content_type)
    self.assertFalse(same_content_type)
