# -*- coding: utf-8 -*-

import config
import telebot
import random

bot = telebot.TeleBot(config.token)
start = False
enemyv = 0
n = str()
fuck = 0
score = 0
pd = {}
wds = str()

def getid(text):
    fuck = ""
    for i in text.split():
        if i.isdigit():
            fuck += str(i)
    global n
    if fuck == "":
        n == 0
    else:
        n = fuck
    fuck = 0
    return(n)

@bot.message_handler(commands=["start", "help"])
def welcome(message):
    bot.send_message(message.chat.id, "Welcome to Guess My Word!\nThis is the game for expanding your vocabulary!\n\n"
                                      "Here are the commands to control the game:\n\n"
                                      "/rules - Display the rules of the game\n"
                                      "/newgame - Register a new player\n"
                                      "/rival XXX - where Xs are your rival ID, for which you ask him or her\n"
                                      "/w your_word - Submit a word to a competition\n"
                                      "/a your_answer - Submit your answer\n"
                                      "/score - Display scores\n"
                                      "/feedback Your_message - Send your message to developers")


@bot.message_handler(commands=["rules"])
def rules(message):
    bot.send_message(message.chat.id, "Welcome to Guess My Word v.1 !\nThis is the game for fun and expanding your vocabulary!\n\n"
                                      "Now it is designed for two-player mode and has the following rules:\n\n"
                                      "A player starts new game with /newgame command. After that he or she "
                                      "is asked to swap ID's with a rival. Received ID is submited as /rival XXXXXX. "
                                      "The game is now started and each of the rivals shares a word with the Bot using \"/w your_word\" command. "
                                      "The letters in the word are mixed randomly and the result is sent to the rival. "
                                      "The aim of each player is to disclose the encrypted word. To submit an answer \"/a your_answer\" command is used. "
                                      "Successful guess gives 1 point. Unsuccessful attempt gives 0 points. The player has one attempt only.\n"
                                      "Enjoy your game!")


@bot.message_handler(commands=["newgame", "play"])
def ID(message):
    global pd
    pd[message.chat.id] = [0,0,"",0,1,[],0]
    bot.send_message(message.chat.id, "Hi! You are now registered in the game.\n\nHere is your ID:\nPlease send it to your rival. \nI also need an ID you received from your enemy in the following format: \n/rival XXXXXX")
    bot.send_message(message.chat.id, message.chat.id)
    print(pd)


@bot.message_handler(commands=["rival"])
def enemy(message):
    if message.chat.id in pd:
        getid(message.text)
        pd[message.chat.id][0] = n
        global n
        n = ""
        bot.send_message(message.chat.id, "Thanks! Now I am ready to receive your word.\nThe format is:  \n/w your_word")
        if int(pd[message.chat.id][0]) in pd:
            if pd[int(pd[message.chat.id][0])][2] != "" and pd[int(pd[message.chat.id][0])][0] == str(message.chat.id):
                bot.send_message(message.chat.id, "And it looks like you got a call from your rival! You can answer using /a . Here is the word he have sent.")
                bot.send_message(message.chat.id, pd[int(pd[message.chat.id][0])][2])
                pd[message.chat.id][2] = ""
                pd[message.chat.id][5] = []
        else:
            bot.send_message(int(pd[message.chat.id][0]), "Hey! You've just got an invitation from user " + str(message.chat.id) + "To play with him just press here> /play and type /rival USER_ID .")
    else:
        bot.send_message(message.chat.id, "Please, start the game first using /play . You need to register.")
    print(pd)


@bot.message_handler(commands=["w"])
def myrand(message):
    global pd
    if message.chat.id in pd:
        if pd[message.chat.id][4] == 1:
            bot.send_message(message.chat.id, "OK, I got your word and will send it to your rival as soon as he is registered.")
            pd[message.chat.id][1] = message.text[3:]
            print(message.chat.id)
            if message.text[3:].casefold() == "артемий":
                bot.send_message(message.chat.id, "ХахАх Лапл")
            global pd
            pd[message.chat.id][5] = [i for i in pd[message.chat.id][1]]
            random.shuffle(pd[message.chat.id][5])
            for i in pd[message.chat.id][5]:
                global pd
                pd[message.chat.id][2] += i.casefold()
                pd[message.chat.id][4] = 0
            if int(pd[message.chat.id][0]) in pd and pd[int(pd[message.chat.id][0])][0] == str(message.chat.id):
                bot.send_message(pd[message.chat.id][0], pd[message.chat.id][2])
                pd[message.chat.id][2] = ""
                pd[message.chat.id][5] = []
            else:
                bot.send_message(message.chat.id, "BOT IS BEING UNDER CONSTRUCTIOИ\nPlease, report bugs via /feedback Your_message.")
            print(pd)
        else:
            bot.send_message(message.chat.id, "Please, wait until your rival makes an attempt")
    else:
        bot.send_message(message.chat.id, "Please, start the game first using /play . You need to register.")
        return(0)



@bot.message_handler(commands=["a"])
def answ(message):
    global pd
    if message.chat.id in pd:
        global pd
        pd[message.chat.id][6] = message.text[3:]
        print(pd)
        if pd[message.chat.id][6].casefold() == pd[int(pd[message.chat.id][0])][1].casefold():
            global pd
            pd[message.chat.id][3] += 1
            bot.send_message(message.chat.id,"Right! The word was: \n")
            bot.send_message(message.chat.id, pd[int(pd[message.chat.id][0])][1])
            bot.send_message(int(pd[message.chat.id][0]), "Sorry, but your rival has guessed the word \"" + str(pd[int(pd[message.chat.id][0])][1]) + "\"")
            global pd
            pd[int(pd[message.chat.id][0])][1] = ""
            pd[int(pd[message.chat.id][0])][2] = ""
            pd[int(pd[message.chat.id][0])][4] = 1
            print(pd)
            return()
        elif pd[int(pd[message.chat.id][0])][4] == 0:
            bot.send_message(message.chat.id, "Nope! The word was: \n")
            bot.send_message(message.chat.id, pd[int(pd[message.chat.id][0])][1])
            bot.send_message(int(pd[message.chat.id][0]), "Yeah, your rival has not succeeded. \"" + str(pd[int(pd[message.chat.id][0])][1]) + "\"")
            global pd
            pd[int(pd[message.chat.id][0])][1] = ""
            pd[int(pd[message.chat.id][0])][2] = ""
            pd[int(pd[message.chat.id][0])][4] = 1
        elif pd[int(pd[message.chat.id][0])][4] == 1:
            bot.send_message(message.chat.id, "Your variant has been already submitted")
            print(pd)
            return(0)


@bot.message_handler(commands=["score"])
def score(message):
    if message.chat.id in pd:
        bot.send_message(message.chat.id, ["Your score is " + str(pd[message.chat.id][3])])


@bot.message_handler(commands=["feedback"])
def feedback(message):
    bot.send_message(3755631, "Feedback from chat " + str(message.chat.id) + "\n" + message.text[10:])
    bot.send_message(message.chat.id, "Your feedback was sent to FRONT END DEVELOPER ARTEMII, thank you.")
if 0 == 0:
    bot.polling(none_stop=True)
