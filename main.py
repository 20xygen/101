import time
import random
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from BOT1 import bot
class bot_cummunication:
    async def checker(self, id):
        f = open("test.txt", "r+")
        st = time.time()
        string = time.asctime() + " начал рабочий день\n"
        flag = 2
        с = 0
        while True:
            if flag == 0:
                break
            elif flag == 1:
                s = str(input())
                if s == "Продолжить":
                    flag = 2
                    b = time.time()
                    с += b - a
                    string += time.asctime() + " закончил перерыв, длившийся " + str(int((b - a) / 60)) + " минут\n"
                    continue
            while True:
                flag = False
                x = time.time()
                await bot.send_message(id, "Ты работаешь?")
                #----------
                s = str(input())
                if s == "Да":
                    y = time.time()
                    if y - x > 5:
                        print("Вы не работаете, сохраняю")
                        string += time.asctime() + " НЕ работает, отмазка: " + s + "\n"
                    else:
                        string += time.asctime() + " работает" + "\n"
                elif s == "Пауза":
                    y = time.time()
                    flag = 1
                    a = time.time()
                    string += time.asctime() + " взял перерыв спустя " + str(int((y - x))) + " секунд бездействия\n"
                    print("Для возобновления работы напишите \"Продолжить\"")
                    break
                elif s == "Завершить":
                    flag = 0
                    break
                else:
                    y = time.time()
                    if y - x > 5:
                        print("Вы не работаете, сохраняю")
                        string += time.asctime() + " НЕ работает, отмазка: " + s + "\n"
                    else:
                        print("Сохраняю сообщение")
                        string += time.asctime() + " сообщил \"" + s + "\" через " + str(int((y - x))) + " секунд\n"
                t = random.uniform(2, 7)
                time.sleep(t)
        string += time.asctime() + \
                      " закончил рабочий день (провел за работой " + str(int((time.time() - st - с) / 3600)) + \
                      " часов " + str(int(((time.time() - st - с) % 3600) / 60)) + " минут)\n"
        print(string)
        f.write(string)
        f.close()

    def print_bot(self, text, id):
        await bot.send_message(id, text)

class buttons:
    worker_or_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    worker = KeyboardButton(text="Работник")
    admin = KeyboardButton(text="Админ")
    worker_or_admin.add(worker, admin)
