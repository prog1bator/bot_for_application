from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,\
    KeyboardButton, ReplyKeyboardMarkup

kb_button = [
    [KeyboardButton(text='Профиль')],
    [KeyboardButton(text='Информация')],
    [KeyboardButton(text='Связь')],
    [KeyboardButton(text='Тест')],
    [KeyboardButton(text='Выход')]
]
kb_menu = ReplyKeyboardMarkup(
    keyboard=kb_button,
    resize_keyboard=True,
)

kbb = ReplyKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Меню'))

for_admin = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Принять', callback_data='accept'),
    InlineKeyboardButton(text='Отклонить', callback_data='reject')
)