import logging
import time
import random
import db
from aiogram import Bot, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.filters import Text

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5140537236:AAGhmSgBezgLfxMu1Gv9YdaP0e3J5nRcZzA'

# webhook settings
WEBHOOK_URL = 'https://08cc-85-143-113-146.ngrok.io'
WEBHOOK_PATH = ''
WEBHOOK_HOST = "127.0.0.1"
WEBHOOK_PORT = 5000
# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 1234

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands="start")
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, "Здравствуйте, вы вошли в число людей, у которых замечана подозрительная активность во время рабочего процесса")
    worker_or_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    worker = KeyboardButton(text="Работник")
    admin = KeyboardButton(text="Админ")
    worker_or_admin.add(worker, admin)
    await bot.send_message(message.chat.id, "Вы работник или админ?", reply_markup=worker_or_admin)


@dp.message_handler()
async def echo(message: types.Message):
    rows = db.sql.execute('''SELECT id FROM users''').fetchall()
    rows_idnew = [i[0] for i in rows]
    f = 0
    print(message)
    for i in rows_idnew:
        if i == message.chat.id:
            f = 1
    if f == 0:
        if message.text == "Работник":

            await bot.send_message(message.chat.id, "Выберите вашего админа", reply_markup=choose_admins())
            #db.sql.execute('''INSERT INTO users (id, status, admin_id) VALUES (?, ?, ?)''', (message.chat.id, 0, ))
        elif message.text == "Админ":
            db.sql.execute('''INSERT INTO users (id, username, status, admin_id) VALUES (?, ?, ?, ?)''', (message.chat.id, message.chat.username, 1, None))
    else:
        await bot.send_message(message.chat.id, "Вы уже есть в базе данных")


@dp.callback_query_handler(Text(startswith='admin_'))
async def results(call: types.CallbackQuery):
    db.sql.execute(f'''UPDATE users SET admin_id = ? WHERE id = ?''',(call.data[6:], call.message.chat.id))
    await bot.send_message(call.message.chat.id, "Теперь за вами следят")

def choose_admins():
    rows = db.sql.execute('''SELECT id, username FROM users WHERE status = 1''').fetchall()
    rows_idnew = [i[0] for i in rows]
    rows_namenew = [i[1] for i in rows]
    admins = InlineKeyboardMarkup()
    for i in range(len(rows_idnew)):
        admin = InlineKeyboardButton(text=rows_namenew[i], callback_data=f'admin_{rows_idnew[i]}')
        admins.add(admin)
    return admins


#-------------------------------------------------------------------
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )