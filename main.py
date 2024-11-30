import io
from zipfile import ZipFile
import os
import shutil

from settings import settings
from telebot import TeleBot
from .codemate.application.composer import Composer

PATH_TO_SAVE_PROJECTS = "/home/root/hack_projects/"

# Функция для обработки файлов и создания репортов
def process_file(file) -> str:
    report = report = Composer().create_report_for_file(file)
    return report


# Функция для обработки архивов
def process_archive(zip_file):
    zip_name = os.path.basename(zip_file).rsplit('.')[1]
    project_path = PATH_TO_SAVE_PROJECTS + zip_name
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    
    with ZipFile(io.BytesIO(zip_file), 'r') as zip_ref:
        zip_ref.extractall(project_path)

    report = Composer().create_report_for_project(project_path)
    return report

# Создание бота и обработка сообщений
bot = TeleBot(settings.tg_token)


@bot.message_handler(content_types=['document'])
def handle_document(message):
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


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я бот для проверки проектов. Отправьте мне файл или архив для обработки.")


@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Я не знаю, что делать с этим. Пожалуйста, отправьте мне файл или архив для обработки.")


if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()
