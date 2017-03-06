import config
import telebot
import time
import urllib
from random import randint
import sqlite3



bot = telebot.TeleBot(config.token)
numbo = 0

def get_random_sticker():
    global numbo
    numbo = randint(0, 2309)
    conn = sqlite3.connect("example.db")
    cc = conn.cursor()
    data = cc.execute("SELECT * FROM stickers WHERE id =" + str(numbo)).fetchone()
    conn.close
    return data

def get_sticker_by_id(id):
    id = str(id)
    conn = sqlite3.connect("example.db")
    cc = conn.cursor()
    data = cc.execute("SELECT * FROM stickers WHERE id =" + id).fetchone()
    conn.close
    return data

def read_rating(message):
    rating = int(message.text)



@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Введите /next")

@bot.message_handler(commands=['next'])
def send_welcome(message):
    list_sticker = get_random_sticker()
    reply = str(list_sticker[0]) + "\n" + list_sticker[1] + "\n" + list_sticker[2] + "\n" + list_sticker[3] + "\n" + "Рейтинг " + str(list_sticker[4])
    bot.reply_to(message, reply)

@bot.message_handler(content_types=['text'])
def set_rating(message):
    try:
        kek = int(message.text)
    except:
        bot.reply_to(message, "Введите число")
    else:
        list_sticker = get_sticker_by_id(numbo)
        rating = list_sticker[4]
        timesrated = list_sticker[5]
        try:
            timesrated += 1
            rating += kek
            rating = rating/timesrated
        finally:
            conn = sqlite3.connect("example.db")
            cc = conn.cursor()
            listicle = []
            listicle.append((rating, timesrated, numbo))
            cc.executemany("UPDATE stickers SET rating = ?, timesrated = ? WHERE id=?", listicle)
            conn.commit()
            conn.close()
            bot.reply_to(message, "Новый рейтинг стикера: " + str(rating))




@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

try:
    bot.polling(none_stop=True)

    # ConnectionError and ReadTimeout because of possible timeout of the requests library
    # maybe there are others, therefore Exception

except Exception as e:
        logger.error(e)
        time.sleep(15)
