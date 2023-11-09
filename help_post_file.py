# Файл для отправки POST запроса на http://localhost:8000/upload/
import requests

url = 'http://localhost:8000/upload/'
file_name = 'test.pdf'  # имя файла
file_path = '/Users/applestock/Downloads/test.pdf'  # путь к файлу
files = {'file': (file_name, open(file_path, 'rb'))}

response = requests.post(url, files=files)

if response.status_code == 201:
    print('Файл успешно загружен!')
else:
    print('Ошибка при загрузке файла:', response.status_code)

