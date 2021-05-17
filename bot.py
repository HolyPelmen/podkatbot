import telebot
import config
import database as db
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

connection = db.create_connection("localhost", "root", "Vladsuper2001", "Base")

def selectUpperCaseFromBase (id):
    result = db.execute_read_queryString(connection, "SELECT UpperCase FROM Compliments WHERE ID = {}".format(id))
    return result
    
def selectLowerCaseFromBase (id):
    result = db.execute_read_queryString(connection, "SELECT LowerCase FROM Compliments WHERE ID = {}".format(id))
    return result

def selectUpperCaseBoysFromBase (id):
    result = db.execute_read_queryString(connection, "SELECT UpperCaseBoys FROM Compliments WHERE ID = {}".format(id))
    return result
    
def selectLowerCaseBoysFromBase (id):
    result = db.execute_read_queryString(connection, "SELECT LowerCaseBoys FROM Compliments WHERE ID = {}".format(id))
    return result
    
def randID():
    result = random.randint(1, 85)
    return result

@bot.inline_handler(lambda query: query.query == '')
def query_podkat(inline_query): 
    try:
        rand_id = randID()
        r = types.InlineQueryResultArticle(
            id = '1', title = 'Подкат', description = 'Подкати, не ссы.',
            input_message_content = types.InputTextMessageContent("{}".format(selectUpperCaseFromBase(rand_id)))
        )
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)

@bot.message_handler(commands=['start'])
def start(message):
    button1 = types.KeyboardButton("Подкат к девушке")
    button2 = types.KeyboardButton("Подкат к парню")
    button3 = types.KeyboardButton("Фотоподкат к девушке")
    button4 = types.KeyboardButton("Фотоподкат к парню")
    markup = types.ReplyKeyboardMarkup(row_width = 2).add(
        button1, button2,
        button3, button4
    )
    bot.send_message(message.chat.id, 'Создан, чтобы служить вам', reply_markup=markup)

@bot.message_handler(commands=['podkat'])
def podkat(message):
    rand_id = randID()
    if len(message.entities) > 1:
        enti = message.entities[1]
        if (enti.type == 'text_mention' and enti.user.is_bot==False):
            user_id = enti.user.id  
            user_name = enti.user.first_name
            mention = "["+user_name+"](tg://user?id="+str(user_id)+")"
                
            bot.send_message(message.chat.id, mention + "{}".format(selectLowerCaseFromBase(rand_id)), parse_mode = 'Markdown')
        elif enti.type == "mention":
            menText = message.text
            bot.send_message(message.chat.id, menText[8:] + "{}".format(selectLowerCaseFromBase(rand_id)))
    else:
        bot.send_message(message.chat.id, format(selectUpperCaseFromBase(rand_id)), reply_to_message_id=message.message_id)

@bot.message_handler(content_types=["new_chat_members"])
def podkatEnter(message):
    rand_id = randID()
    user_name = message.new_chat_member
    bot.send_message(message.chat.id, format(selectUpperCaseFromBase(rand_id)), reply_to_message_id=message.message_id)

@bot.message_handler(content_types=['text'])
def podkatPrivate(message):
    rand_id = randID()
    if message.chat.type == 'private':
        if message.text == "Подкат к девушке":
            bot.send_message(message.chat.id, format(selectUpperCaseFromBase(rand_id)))
        elif message.text == "Подкат к парню":
            bot.send_message(message.chat.id, format(selectUpperCaseBoysFromBase(rand_id)))

bot.polling(none_stop=True)