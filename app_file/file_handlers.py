import os
from datetime import datetime
import logging

from PIL import Image
import magic
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def upload_and_process_file(file):
    """
    Функция определения типа файла и выбора обработчика

    :param file: загруженный файл
    """
    logger.info(f"Начало выполнения задачи для файла: {file.name}")

    mime_type = magic.from_file(file.name)
    if 'image' in mime_type:
        return process_image(file)
    elif 'text' in mime_type:
        return process_text(file)
    elif 'PDF' in mime_type:
        return process_pdf(file)
    else:
        return process_other_file(file)


def process_image(file):
    """
    Функция обработки Image файлов

    :param file: загруженный файл
    :return: черно-белый переименованный файл, с указанием времени обработки,
    помещается в папку image.
    """

    image = Image.open(file)  # Открываем изображение
    bw_image = image.convert('L')  # Конвертируем в черно-белый формат
    bw_image.save(file.name)  # Сохраняем обработанное изображение

    time_processed = datetime.now().strftime('%-y-%-m-%d-%H-%M')
    file_name = os.path.basename(file.name)
    new_name = time_processed + file_name
    os.rename(file.name, new_name)

    if not os.path.isdir('uploads/image'):
        os.mkdir('uploads/image')
    os.replace(new_name, f'uploads/image/{new_name}')  # Переименовываем файл и переносим в папку image

    logger.info(f"Успешно обработан файл {new_name}.")

    return f'uploads/image/{new_name}'  # Возвращаем путь к обработанному файлу


def process_pdf(file):
    """
    Функция обработки PDF файлов

    :param file: загруженный файл
    :return: переименованный файл PDF, с указанием времени обработки,
    помещается в папку PDF, текст файла в формате .txt помещается в папку txt_from_PDF.
    """

    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()  # извлекаем текст из PDF

    time_processed = datetime.now().strftime('%-y-%-m-%d-%H-%M')

    file_name_without_type = os.path.splitext(os.path.basename(file.name))[0]
    file_dir_txt = f'uploads/txt_from_PDF/{time_processed}_{file_name_without_type}.txt'

    if not os.path.isdir('uploads/txt_from_PDF'):
        os.mkdir('uploads/txt_from_PDF')  # создаем папку txt_from_PDF, если ее нет

    with open(file_dir_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)  # записываем текст в .txt

    time_processed = datetime.now().strftime('%-y-%-m-%d-%H-%M')
    file_name = os.path.basename(file.name)
    new_name = f'{time_processed}_{file_name}'
    os.rename(file.name, new_name)

    if not os.path.isdir('uploads/PDF'):
        os.mkdir('uploads/PDF')

    os.replace(new_name, f'uploads/PDF/{new_name}')  # Переименовываем файл и переносим в папку PDF

    logger.info(f"Успешно обработан файл {new_name}.")

    return f'uploads/PDF/{new_name}'  # Возвращаем путь к обработанному файлу


def process_text(file):
    """
    Функция обработки текстовых файлов

    :param file: загруженный файл
    :return: Изменяем текст файла так, чтобы он был написан заглавными буквами.
    Переименованный файл txt, с указанием времени обработки, помещается в папку txt.
    """

    with open(file.name, 'r') as f:
        lines = f.readlines()

    lines = [line.upper() for line in lines]  # Преобразуем текст в верхний регистр

    with open(file.name, 'w') as f:
        f.writelines(lines)  # Пишем текст в файл

    time_processed = datetime.now().strftime('%-y-%-m-%d-%H-%M')
    file_name = os.path.basename(file.name)
    new_name = f'{time_processed}_{file_name}'
    os.rename(file.name, new_name)

    if not os.path.isdir('uploads/text'):
        os.mkdir('uploads/text')
    os.replace(new_name, f'uploads/text/{new_name}')  # Переименовываем файл и переносим в папку text

    logger.info(f"Успешно обработан файл {new_name}.")

    return f'uploads/text/{new_name}'  # Возвращаем путь к обработанному файлу


def process_other_file(file):
    """
    Функция обработки других файлов (не image, txt, pdf)

    :param file: загруженный файл
    :return: Переименованный файл, с указанием времени обработки, помещается в папку other_file.
    """

    time_processed = datetime.now().strftime('%-y-%-m-%d-%H-%M')
    file_name = os.path.basename(file.name)
    new_name = time_processed + file_name
    os.rename(file.name, new_name)

    if not os.path.isdir('uploads/other_file'):
        os.mkdir('uploads/other_file')

    os.replace(new_name, f'uploads/other_file/{new_name}')  # Переименовываем файл и переносим в папку other_file

    logger.info(f"Успешно обработан файл {new_name}.")

    return f'uploads/other_file/{new_name}'  # Возвращаем путь к обработанному файлу
