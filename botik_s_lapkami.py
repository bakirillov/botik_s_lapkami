import os
import re
import json
import telebot
import requests
import numpy as np
from vedis import Vedis
from pymystem3 import Mystem
from flask import Flask, request

# Initializations
allowed = str(os.environ.get("ALLOWED_USERS", "nobody")).split(",")
TOKEN = str(os.environ.get("BOT_TOKEN", "none"))
WHEREAMI = str(os.environ.get("BOT_ENVIRONMENT", "LOCAL"))
LINK = str(os.environ.get("BOT_LINK", "Ololo"))
bot = telebot.TeleBot(TOKEN)
mstm = Mystem()
server = Flask(__name__)

def authorised(message):
    """"Check if user is authorised"""
    uid = str(message.from_user.id)
    return(uid, uid in allowed)
        
def filter_mystem(x):
    r = True
    if "analysis" not in x:
        r = False
    else:
        if x["analysis"][0]["gr"][0] != "S":
            r = False
    return(r)

@bot.message_handler(commands=["start"])
def greet_and_identify(message):
    g = "Я котик-ботик, у меня лапки-лапки!"
    uid, a = authorised(message)
    if not a:
        g = "Вы котик? Предъявите лапки!"
    bot.reply_to(message, g)
    
@bot.message_handler(content_types=["text"])
def perform_text_operation(message):
    genders = {
        "муж": "был придуман",
        "жен": "была придумана",
        "сред": "было придумано",
    }
    is_change_title = re.search("Лапкочат\s.+\sGANG", message.text)
    try:
        if is_change_title:
            bot.send_chat_action(message.chat.id, "typing")
            bot.set_chat_title(message.chat.id, is_change_title[0])
        if np.random.choice([True, False], p=[0.05, 0.95]):
            bot.send_chat_action(message.chat.id, "typing")
            analysis = mstm.analyze(message.text)
            not_empty = list(filter(filter_mystem, analysis))
            if len(not_empty) > 0:
                chosen = np.random.choice(np.arange(len(not_empty)))
                word = not_empty[chosen]["analysis"][0]["lex"]
                splat_gr = not_empty[chosen]["analysis"][0]["gr"].split(",")
                gender = splat_gr[1] if "обсц" not in splat_gr[1] else splat_gr[2] 
                gendered = genders[gender]
                bot.reply_to(
                    message, 
                    "Напоминаю, что "+word+" "+gendered+" Собором для захвата и удержания власти. \n\n Ваш NRx-котик."
                )
    except Exception as e:
        bot.reply_to(message, str(e))
        
@server.route('/'+TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return("!", 200)

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=LINK+TOKEN)
    return("!", 200)

if WHEREAMI == "HEROKU":
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
else:
    bot.polling(none_stop=True)