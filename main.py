import io
from zipfile import ZipFile
import os

from requests import HTTPError

from settings import settings
from telebot import TeleBot
from codemate.application.composer.composer import Composer

PATH_TO_SAVE_PROJECTS = "unziped/"

# Функция для обработки файлов и создания репортов
def process_file(file) -> str:
    report = report = Composer().create_report_for_file(file)
    return report


def unzip_bytes_to_directory(zip_bytes, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create a BytesIO object from the zip bytes
    zip_buffer = io.BytesIO(zip_bytes)

    # Open and extract the zip file
    with ZipFile(zip_buffer, 'r') as zip_ref:
        # Extract all files to the output directory
        zip_ref.extractall(output_dir)
        # Get list of all files in the zip
        extracted_files = zip_ref.namelist()

    return extracted_files

# Функция для обработки архивов
def process_archive(zip_file):
    extracted_files = unzip_bytes_to_directory(zip_file, PATH_TO_SAVE_PROJECTS)
    project_path = PATH_TO_SAVE_PROJECTS
    report = Composer().create_report_for_project(project_path)
    return report

# Создание бота и обработка сообщений
bot = TeleBot(settings.tg_token)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        if message.document.file_name.endswith('.zip'):
            result_report = process_archive(downloaded_file)
            r_type = "архив"
        else:
            result_report = process_file(downloaded_file)
            r_type = "файл"

        bot.reply_to(message, f"Ваш {r_type} был обработан, результаты прикреплены к сообщению.")
        with open(result_report, "rb") as report_file:
            bot.send_document(chat_id=message.chat.id, document=report_file)
    except HTTPError as http_e:
        bot.reply_to(message, f"Проблема с моделью - {http_e}")



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я бот для проверки проектов. Отправьте мне файл или архив для обработки.")


@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Я не знаю, что делать с этим. Пожалуйста, отправьте мне файл или архив для обработки.")


if __name__ == '__main__':
    os.mkdir(PATH_TO_SAVE_PROJECTS)
    print("Bot started")
    bot.infinity_polling()
