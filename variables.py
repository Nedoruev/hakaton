from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from gino import Gino
from data import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os


BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

login_text = 'Щоб зареєструватися ' \
             'напишіть\n"Login" ' \
             '/ "Password"\nвідповіддю на це повідомлення.'

sup_text = 'Для входу у систему напишіть ' \
           '\n"Login" / "Password"\nвідповіддю ' \
           'на це повідомлення.'

c_name_text = 'Напишіть "Старе ім\'я" / "Нове ім\'я"' \
              '\nвідповіддю на це повідомлення.'

c_disc_text = 'Напишіть "Ім\'я" / "Нова дисципліна"' \
              '\nвідповіддю на це повідомлення.'

c_disc_name_text = 'Напишіть "Стара дисципліна" / "Нова дисципліна"' \
                   '\nвідповіддю на це повідомлення.'

c_disc_info_text = 'Напишіть "Дисципліна" / "Нова інформація"' \
                   '\nвідповіддю на це повідомлення.'
disc_students_text = 'Напишіть назву дисципліни' \
                   '\nвідповіддю на це повідомлення.'

c_disc_info_t_text = 'Напишіть нову інформацію' \
                   '\nвідповіддю на це повідомлення.'

register_text = 'Напишіть назву дисципліни, на яку бажаєте зареєструватись, ' \
                'відповіддю' \
                ' на це повідомлення'


db = Gino()

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)

scheduler = AsyncIOScheduler()

scheduler.start()

load_dotenv()

admin_main_menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Профіль', callback_data='profile')],
    [InlineKeyboardButton('Викладачі', callback_data='teachers')],
    [InlineKeyboardButton('Дисципліни', callback_data='disc1')]])

admin_t_menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Змінити ім\'я', callback_data='c_name')],
     [InlineKeyboardButton('Змінити дисципліни', callback_data='c_disc')],
     [InlineKeyboardButton('Головне меню', callback_data='main_menu')]])

admin_d_menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Змінити назву', callback_data='c_d_name')],
     [InlineKeyboardButton('Змінити інформацію', callback_data='c_info')],
     [InlineKeyboardButton('Студенти', callback_data='students')],
     [InlineKeyboardButton('Головне меню', callback_data='main_menu')]])

teacher_menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Профіль', callback_data='profile')],
    [InlineKeyboardButton('Дисципліна', callback_data='t_dis')],
    [InlineKeyboardButton('Редагувати інф-ю про дисципліну', callback_data='teacher2')],
    [InlineKeyboardButton('Студенти', callback_data='teacher1')]])

student_menu = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton('Профіль', callback_data='profile')],
    [InlineKeyboardButton('Дисципліни', callback_data='123123')]])

student_disc_menu = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
                    [InlineKeyboardButton('Зареєструватись', callback_data='register')],
                    [InlineKeyboardButton('Головне меню', callback_data='321321')]])