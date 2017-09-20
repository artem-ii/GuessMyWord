__author__ = 'artemii'
import telebot
import newbotconfig
bot = telebot.TeleBot(newbotconfig.token)
@bot.message_handler(content_types = ["text"])
def smth(message):
    from telebot import types
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('a')
    itembtn2 = types.KeyboardButton('v')
    itembtn3 = types.KeyboardButton('d')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)
    bot.send_message(message.chat.id, (bot.get_chat(message.chat.id)).username + message.chat.first_name)
    print(bot.get_updates())
    #bot.send_message(message.chat.id, bot.get_updates())



bot.polling(none_stop = True)
