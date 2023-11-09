import os
import shutil
from PIL import Image

from django.test import TestCase

from ..models import File
from ..file_handlers import process_other_file, process_text, process_pdf, process_image


class ProcessImageTest(TestCase):

    def setUp(self):
        shutil.copy2('app_file/tests/fixtures/test.jpeg', 'app_file/tests/fixtures/test_copy.jpeg')
        self.path_test_pdf_file = 'app_file/tests/fixtures/test_copy.jpeg'
        self.file_data = File.objects.create(file=self.path_test_pdf_file, processed=False)

    def test_process_image(self):
        processed_file_path = process_image(self.file_data.file)

        # Проверяем, что файл был переименован и сохранен в нужную папку
        self.assertTrue(os.path.exists(processed_file_path))
        self.assertIn('uploads/image/2', processed_file_path)

        # ПРоверяем, изменилось ли изображение на черно-белое
        image = Image.open(self.file_data.file)
        bw_image = image.convert('L')
        path_bw_image = 'uploads/image/bw_image_test.jpeg'
        bw_image.save(path_bw_image)
        bw_image_colors = bw_image.getcolors()
        image_colors = image.getcolors()
        self.assertEqual(image_colors, bw_image_colors)

        # Удаляем полученные файлы после теста
        os.remove(processed_file_path)
        os.remove(path_bw_image)


class ProcessPDFTest(TestCase):

    def setUp(self):
        shutil.copy2('app_file/tests/fixtures/test.pdf', 'app_file/tests/fixtures/test_copy.pdf')
        self.path_test_pdf_file = 'app_file/tests/fixtures/test_copy.pdf'
        self.file_data = File.objects.create(file=self.path_test_pdf_file, processed=False)

    def test_process_pdf(self):
        processed_file_path = process_pdf(self.file_data.file)

        # Проверяем, что файл был переименован и сохранен в нужную папку
        self.assertTrue(os.path.exists(processed_file_path))
        self.assertIn('uploads/PDF/2', processed_file_path)

        file_name_without_type = os.path.splitext(os.path.basename(processed_file_path))[0]
        txt_file_name = f'{file_name_without_type}.txt'
        directory_txt_from_pdf = 'uploads/txt_from_PDF/'
        # Получаем список файлов txt_from_PDF
        files = os.listdir(directory_txt_from_pdf)
        self.assertIn(txt_file_name, files)

        # Удаляем полученные файлы после теста
        os.remove(processed_file_path)
        os.remove(directory_txt_from_pdf + txt_file_name)


class ProcessTextTest(TestCase):

    def test_process_text(self):
        # Создайте временный файл и записываем в него тестовые данные
        text_for_file = 'This is a test file.'

        with open('temp_text.txt', 'w') as temp_file:
            temp_file.write(text_for_file)

        file_data = open('temp_text.txt', 'rb')
        processed_file_path = process_text(file_data)

        # Проверяем, что текст в файле переведен в верхний регистр
        with open(processed_file_path, 'r') as f:
            lines = f.readlines()

        lines = [line.upper() for line in lines]
        self.assertEqual(lines[0], text_for_file.upper())

        # Проверяем, что файл был переименован и сохранен в нужную папку
        self.assertTrue(os.path.exists(processed_file_path))
        self.assertIn('uploads/text/2', processed_file_path)

        # Удаляем временный файл после теста
        file_data.close()
        os.remove(processed_file_path)


class ProcessOtherFileTest(TestCase):

    def test_process_other_file(self):
        # Создаем временный файл и записываем в него тестовые данные
        with open('temp_other.txt', 'w') as temp_file:
            temp_file.write("This is a test file.")

        file_data = open('temp_other.txt', 'rb')
        res = process_other_file(file_data)

        # Проверяем, что файл был переименован и перемещен
        self.assertTrue(os.path.exists(res))

        # Удаляем временный файл после теста
        file_data.close()
        os.remove(res)
