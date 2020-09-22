import telebot
import config
import base
import base_small
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.inline_handler(lambda query: query.query == '')
def query_podkat(inline_query): 
    try:
        r = types.InlineQueryResultArticle(
            id = '1', title = 'Подкат', description = 'Подкати, не ссы.',
            input_message_content = types.InputTextMessageContent(random.choice(base.podkat_list))
        )
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Подкат😏")
    markup.add(button1)
    bot.send_message(message.chat.id, 'Создан, чтобы служить вам', reply_markup=markup)

@bot.message_handler(commands=['podkat'])
def podkat(message):
    if len(message.entities) > 1:
        enti = message.entities[1]
        if (enti.type == 'text_mention' and enti.user.is_bot==False):
            user_id = enti.user.id  
            user_name = enti.user.first_name
            mention = "["+user_name+"](tg://user?id="+str(user_id)+")"
                
            bot.send_message(message.chat.id, mention + random.choice(base_small.podkat_list), parse_mode = 'Markdown')
        elif enti.type == "mention":
            menText = message.text
            bot.send_message(message.chat.id, menText[8:] + random.choice(base_small.podkat_list))
    else:
        bot.send_message(message.chat.id, random.choice(base.podkat_list), reply_to_message_id=message.message_id)

@bot.message_handler(content_types=["new_chat_members"])
def podkatEnter(message):
    user_name = message.new_chat_member
    bot.send_message(message.chat.id, random.choice(base.podkat_list), reply_to_message_id=message.message_id)

@bot.message_handler(content_types=['text'])
def podkatPrivate(message):
    if message.chat.type == 'private':
        if message.text == "Подкат😏":
            bot.send_message(message.chat.id, random.choice(base.podkat_list))

bot.polling(none_stop=True)