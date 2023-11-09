import os

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from ..models import File
import logging

logger = logging.getLogger(__name__)


class FileUploadViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {'file': ('test.jpeg', open('app_file/tests/fixtures/test.jpeg', 'rb'))}

    def test_upload_file(self):
        response = self.client.post('/upload/', self.valid_payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка, что файл был успешно добавлен и не обработан
        self.assertEqual(File.objects.count(), 1)
        self.assertEqual(File.objects.get().processed, False)
        os.remove('uploads/test.jpeg')

    def test_upload_invalid_file(self):
        invalid_payload = {'file': 'fixtures/invalid.txxx'}  # Замените на некорректные данные
        response = self.client.post('/upload/', invalid_payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FileListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.file1 = File.objects.create(file='file1.txt', processed=True)
        self.file2 = File.objects.create(file='file2.txt', processed=False)

    def test_get_files(self):
        response = self.client.get('/files/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
