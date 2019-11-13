import os
import re
import json
import telebot
import requests
import numpy as np
import pandas as pd
from vedis import Vedis
from github3 import login
from pymystem3 import Mystem
from flask import Flask, request


# Initializations
allowed = str(os.environ.get("ALLOWED_USERS", "nobody")).split(",")
TOKEN = str(os.environ.get("BOT_TOKEN", "none"))
WHEREAMI = str(os.environ.get("BOT_ENVIRONMENT", "LOCAL"))
LINK = str(os.environ.get("BOT_LINK", "Ololo"))
GIT_LOGIN = str(os.environ.get("GIT_LOGIN", "Ololo"))
GIT_PASS = str(os.environ.get("GIT_PASS", "Ololo"))
GIST_LINK = str(os.environ.get("GIST_LINK", "Ololo"))
CHECHNYA_KRUTO = str(os.environ.get("CHECHNYA_KRUTO", "Мряфъ?"))
bot = telebot.TeleBot(TOKEN)
mstm = Mystem()
server = Flask(__name__)


@bot.message_handler(commands=["listmustreads"])
def list_mustreads(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(
        message, "Списокъ рекомендованной литературы Лапкочата Вы можете найти по ссылкѣ "+GIST_LINK
    )

@bot.message_handler(commands=["tomustreads"])
def add_to_mustreads(message):
    bot.send_chat_action(message.chat.id, "typing")
    try:
        bot.send_message(118365314, str(message.reply_to_message.text))
    except Exception as e:
        bot.reply_to(
            message, "Съ добавленіемъ мастрида произошло фіаско, уфъ: "+str(e)
        )
    else:
        bot.reply_to(
            message, "Новый мастридъ отправленъ на разсмотрѣніе, мррръ"
        )
    
@bot.message_handler(commands=["roll"])
def roll_a_dice(message):
    bot.reply_to(
        message, str(np.random.choice(np.arange(1,7)))
    )

@bot.message_handler(commands=["promote"])
def grant_a_lifetime_nobility(message):
    if message.from_user.id == 118365314:
        user = message.reply_to_message.from_user
        bot.promote_chat_member(
            message.chat.id, user.id, 
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False
        )
        bot.reply_to(
            message, "Высочайшимъ позволеніемъ участнику"+user.username+" даровано личное дворянство, мряфъ."
        )
    else:
        bot.reply_to(message, "Только котикъ съ лапками можетъ даровать личное дворянство и лишать его, муръ.")

@bot.message_handler(commands=["demote"])
def revoke_a_lifetime_nobility(message):
    if message.from_user.id == 118365314:
        user = message.reply_to_message.from_user
        bot.promote_chat_member(
            message.chat.id, user.id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False
        )
        bot.reply_to(message, "Высочайшимъ указомъ "+user.username+"лишается личнаго дворянства.")
    else:
        bot.reply_to(message, "Только котикъ съ лапками можетъ даровать личное дворянство и лишать его, муръ.")
    
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
    g = "Я котикъ-ботикъ, у меня лапки-лапки!"
    uid, a = authorised(message)
    if not a:
        g = "Вы котикъ? Предъявите лапки!"
    bot.reply_to(message, g)
    bot.reply_to(message, str(message.chat.id))
    
@bot.message_handler(content_types=["text"])
def perform_text_operation(message):
    genders = {
        "муж": "былъ придуманъ",
        "жен": "была придумана",
        "сред": "было придумано",
    }
    is_change_title = re.search("Лапкочат\s.+\sGANG", message.text)
    try:
        if is_change_title:
            bot.send_chat_action(message.chat.id, "typing")
            bot.set_chat_title(message.chat.id, is_change_title[0])
        if "бляд" in str(message.text).lower():
            bot.send_chat_action(message.chat.id, "typing")
            bot.reply_to(
                message, "Россія безъ блядства и содоміи!"
            )
        if "ройзман" in str(message.text).lower():
            bot.send_chat_action(message.chat.id, "typing")
            possible_answer = [
                "НАХУЙ РОЙЗМАНА", "Мѣсто Ройзмана на бутылкѣ", "Ройзманъ будетъ люстрированъ",
                "Городъ противъ наркотиковъ = пчелы противъ меда, а Ройзманъ - наркобаронъ",
                "Помни Илью Букатина, помни Сергѣя Костяна."
            ]
            bot.reply_to(
                message, possible_answer[np.random.choice(np.arange(len(possible_answer)))]
            )
        if "чечня" in str(message.text).lower() and "круто" in str(message.text).lower():
            bot.send_chat_action(message.chat.id, "typing")
            bot.reply_to(
                message, CHECHNYA_KRUTO
            )
        if "казахстан" in str(message.text).lower():
            if np.random.choice([True, False], p=[0.3, 0.7]):
                bot.send_chat_action(message.chat.id, "typing")
                bot.reply_to(
                    message, """Мяу! Напоминаю, что правильно говорить "Сырдарьинская и Семиреченская области Туркестанскаго генералъ-губернаторства, Уральская и Тургайская области Оренбургской губерніи, Акмолинская и Семипалатинская области Западно-Сибирскаго генералъ-губернаторства".
                
 Вашъ имперскій котикъ. 
"""
                )
        if np.random.choice([True, False], p=[0.05, 0.95]):
            bot.send_chat_action(message.chat.id, "typing")
            if not re.search("[a-zA-Z]+", message.text):
                try:
                    analysis = mstm.analyze(message.text)
                    not_empty = list(filter(filter_mystem, analysis))
                except:
                    pass
                else:
                    if len(not_empty) > 0:
                        chosen = np.random.choice(np.arange(len(not_empty)))
                        word = not_empty[chosen]["analysis"][0]["lex"]
                        try:
                            gender = re.search("(муж|жен|сред)", not_empty[chosen]["analysis"][0]["gr"])[0]
                        except:
                            gender = None
                        finally:
                            if gender:
                                gendered = genders[gender]
                                bot.reply_to(
                                    message, 
                                        "Мяу! Напоминаю, что "+word+" "+gendered+" Соборомъ для захвата и удержанія власти. \n\n Вашъ NRx-котикъ." 
                                )
            else:
                msgs = [
                    "Если не хочешь оставаться въ тупикѣ, говори со мной только на русскомъ языкѣ, мяу!",
                    "Уберите эти басурманскіе прогрессивные закорючки, не по нраву! Мяу!"
                ]
                bot.reply_to(
                    message, msgs[np.random.choice([0,1])]
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


print(WHEREAMI)
if WHEREAMI == "HEROKU":
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
else:
    bot.polling(none_stop=True)