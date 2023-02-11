# импортируем нужные модули
import logging
import psycopg2
import config
import keyboard
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# создаем бота
bot_token = config.token
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)

# подключаемся к базе данных
connection = psycopg2.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    database=config.db_name
)
connection.autocommit = True

# создаем базу данных
# with connection.cursor() as cursor:
#     cursor.execute(
#         """CREATE TABLE users(
#         user_id BIGINT NOT NULL UNIQUE,
#         true_or_false boolean DEFAULT False,
#         money INT DEFAULT 0,
#         diamond INT DEFAULT 0);"""
#     )


# машина состояний
class Dialog(StatesGroup):
    about_me = State()
    menu = State()
    register = State()


# обработчик команды старт и проверка пользователя на блокировку
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT true_or_false FROM users WHERE user_id = ('{message.from_user.id}') """)
        result = cursor.fetchone()
        if result is None:
            global user_chat_id
            user_chat_id = message.chat.id
            await bot.send_message(message.chat.id, 'заполни заявку\nот 50 до 200 символов')
            await Dialog.register.set()
        elif result[0] == False:
            await bot.send_message(message.chat.id ,'тебя отвергли')
        else:
            await bot.send_message(message.chat.id, 'ты уже в системе, нажми меню', reply_markup=keyboard.kbb)


# проверка правильности заявки
@dp.message_handler(state=Dialog.register)
async def about_user(message: types.Message, state: FSMContext):
    if len(message.text) < 200 and len(message.text) > 50:
        await bot.send_message(config.admin_id, text=\
            f'Заявка от {message.chat.username}\n{message.text}', reply_markup=keyboard.for_admin)
        await message.answer('ваша заявка на рассмотрении, ожидайте')
        await state.finish()
    else:
        await message.answer('форма заполнена неправильно')


# обработчик кнопки принятия и занесение пользователя в базу данных
@dp.callback_query_handler(text_contains='accept')
async def call_accept(call: types.CallbackQuery):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO users(user_id, true_or_false)\
        VALUES ('{user_chat_id}', '{True}');""")
        id = user_chat_id
        await bot.delete_message(chat_id=config.admin_id, message_id=call.message.message_id)
        await bot.send_message(id, text=rf"""вы приняты""")


# обработчик кнопки отклонения и блокировка пользователя
@dp.callback_query_handler(text_contains='reject')
async def call_reject(call: types.CallbackQuery):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO users(user_id, true_or_false)\
        VALUES ('{user_chat_id}', '{False}');""")
        id = user_chat_id
        await bot.delete_message(chat_id=config.admin_id, message_id=call.message.message_id)
        await bot.send_message(id, text=rf"""мы вам перезвоним""")


# обработка кнопок меню
@dp.message_handler(text='Меню')
async def main_menu(message: types.Message):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT true_or_false FROM users WHERE user_id = ('{message.from_user.id}') """)
        result = cursor.fetchone()
        if result[0] == True:
            await message.answer('выберите действие, нажав на кнопку', reply_markup=keyboard.kb_menu)
        elif result[0] == False:
            await message.answer('тебе команда недоступна')


@dp.message_handler(text='Профиль')
async def profile(message: types.Message):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT true_or_false FROM users WHERE user_id = ('{message.from_user.id}') """)
        result = cursor.fetchone()
        if result[0] == True:
            cursor.execute(f"""SELECT money, diamond FROM users WHERE user_id = ('{message.from_user.id}') """)
            # print(cursor.fetchone())
            balance = cursor.fetchone()
            await message.answer(f'твой юзернейм: {message.chat.username}\nтвой никнейм: {message.chat.first_name}\
            \nбаланс монет: {balance[0]}\nбаланс алмазов: {balance[1]}\
            \nнажми Меню, чтобы вернуться', reply_markup=keyboard.kbb)
        elif result[0] == False:
            await message.answer('тебе команда недоступна')


@dp.message_handler(text='Информация')
async def profile(message: types.Message):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT true_or_false FROM users WHERE user_id = ('{message.from_user.id}') """)
        result = cursor.fetchone()
        if result[0] == True:
            await message.answer('сороконожки имеют сорок ножек\nнажми Меню, чтобы вернуться', reply_markup=keyboard.kbb)
        elif result[0] == False:
            await message.answer('тебе команда недоступна')


@dp.message_handler(text='Связь')
async def profile(message: types.Message):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT true_or_false FROM users WHERE user_id = ('{message.from_user.id}') """)
        result = cursor.fetchone()
        if result[0] == True:
            await message.answer('https://t.me/Jorj1o\nнажми Меню, чтобы вернуться', reply_markup=keyboard.kbb)
        elif result[0] == False:
            await message.answer('тебе команда недоступна')


@dp.message_handler(text='Тест')
async def profile(message: types.Message):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT true_or_false FROM users WHERE user_id = ('{message.from_user.id}') """)
        result = cursor.fetchone()
        if result[0] == True:
            await message.answer('все в норме, ты молодец\nнажми Меню, чтобы вернуться', reply_markup=keyboard.kbb)
        elif result[0] == False:
            await message.answer('тебе команда недоступна')


@dp.message_handler(text='Выход')
async def profile(message: types.Message):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT true_or_false FROM users WHERE user_id = ('{message.from_user.id}') """)
        result = cursor.fetchone()
        if result[0] == True:
            await message.answer('до скорых встреч', reply_markup=keyboard.ReplyKeyboardRemove())
        elif result[0] == False:
            await message.answer('тебе команда недоступна')


# обработка любых сообщений пользователя
@dp.message_handler()
async def nothing(message: types.Message):
    if message.from_user.id == config.admin_id:
        await message.answer('ожидайте заявок, мой господин')
    else:
        await message.answer('введите "Меню" если вы в системе\
                             \nили подайте заявку командой /start')

# конструкция запуска программы
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
