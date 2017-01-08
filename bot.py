#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot                  # Bot API Library
from telebot import types       # Bot types API library
import time                     # Library for the time
import feedparser               # Imports the feed reader
import threading                # Library for the counter
import sys                      # Import system libraries
from config import *            # Imports the config file

###################################################################   INIT

# Make the bot
bot = telebot.TeleBot(API_TOKEN)

# Starts the database
#db = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
#cur = db.cursor()
#cur.execute("CREATE TABLE IF NOT EXISTS `latest_topic` ( `id` INT(10) NOT NULL );")
#cur.execute("INSERT INTO latest_topic (id) SELECT '0' WHERE NOT EXISTS (SELECT * FROM latest_topic);")

###################################################################   FUNCTIONS

# Listener
def listener(messages):
    for m in messages:
        cid = m.chat.id
        uid = m.from_user.id
        if m.content_type == 'text': # Sólo saldrán en el log los mensajes tipo texto
            if cid > 0:
                user_message = "New Message: \"" + str(m.from_user.first_name) + " " + str(m.from_user.last_name) + "\" [" + str(cid) + "] -> " + m.text
            else:
                user_message = "New Messsage: \"" + str(m.from_user.first_name) + " " + str(m.from_user.last_name) + "\" [" + str(cid) + "] -> " + m.text
            f = open('log.txt', 'a')
            f.write(user_message + "\n")
            f.close()
            print(user_message)
bot.set_update_listener(listener)

# Has Numbers Checker
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# Update to get the latest topic in RSS
#def update_rss():
#    threading.Timer(60.0, update_rss).start()
#    rss_url = feedparser.parse(rss_feed)
#    print("Fetching RSS...")
#    latest_topic_online = rss_url['entries'][0]['id']
#    latest_topic_online_id = latest_topic_online.replace(FORUM_URL + "-topic-", "")
#    latest_topic_offline = cur.execute("SELECT MAX(id) FROM latest_topic;")
#    for row in cur.fetchall():
#        latest_topic_offline_id = row[0]
#    if int(latest_topic_online_id) > int(latest_topic_offline_id):
#        print("New topic in the community: " + latest_topic_online_id)
#        cur.execute("INSERT INTO latest_topic (id) VALUES (\'" + latest_topic_online_id + "\');")
#        bot.send_message(GROUP_ID, "*New post in the community:* \n\n"
#        "*Title:* " + rss_url['entries'][0]['title'] + "\n" +
#        "*Category:* " + rss_url['entries'][0]['category'] + "\n" +
#        "*Author:* " + rss_url['entries'][0]['author'] + "\n\n" +
#        "_See it _[here](" + FORUM_URL + "/t/" + latest_topic_online + ")",
#        parse_mode="markdown")
#update_rss()

###################################################################   MAIN COMMANDS

# Handle /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """\
Hi there, I the Official Bot of the [""" + FORUM_NAME + "](" + FORUM_URL + """).
Check what I can do using the command /help!\
""", parse_mode="markdown")


# Handle /latest_post
@bot.message_handler(commands=['latest_post'])
def latest_post(message):
    bot.reply_to(message, """
*Unused command* - Use instead `/latest post`
    """, parse_mode="markdown")

# Handle /latest_topic
@bot.message_handler(commands=['latest_topic'])
def latest_post(message):
    bot.reply_to(message, """
*Unused command* - Use instead `/latest topic`
    """, parse_mode="markdown")


# Handle /ping
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "*p*_o_`n`g", parse_mode="markdown")


# Handle /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """
*Hello my friend*
I'm the *official bot of the* [""" + FORUM_NAME + "](" + FORUM_URL + """). I'm here to help you in Telegram to use this community

*List of commands:*
- How to use
  `{foo / boo}` - _Choose one between those options_
  `[number]` - _Compulsory argument_
  `(number)` - _Optional argument_
  `'number'` - _Change 'number' for a real number

- Management Commands
  /start - _Starts me_
  /help - _This command xD_
  /ping - _Checks if the bot is running_

- Feed Commands
/latest `{topic / post / number ['number']}` - _Gives you the _`selection`_ in the forum or the latest _`number`_ of topics_

- Future Commands
  _I will notify in """ + GROUP_NAME + """ when a new topic is released in the forum
  You will be able to read any topic from Telegram_

Any question, just contact to *my creator*: @barreeeiroo
    """, parse_mode="markdown")

# Handle /get_topic
@bot.message_handler(commands=['get_topic'])
def get_topic(message):
    topic_message = message.text
    topic_id = topic_message.replace('/get_topic ','')
    if topic_id == "":
        bot.reply_to(message, "Send me /get\_topic plus the ID of the topic you want to read. _eg.: /get\_topic 123_\nIf you need help finding your topic, checkout the latest 10 topics with the command /latest", parse_mode="markdown")
    else:
        topic_url = FORUM_PROTOCOL + FORUM_URL + "/t/" + topic_id + ".rss"
        topic_rss = feedparser.parse(topic_url)
        print(topic_rss['entries'][0]['title'])
        if message.chat.type != "private":
            bot.reply_to(message, """
*I've sent you the topic in a Private Message*
_Remember to start me in your account to allow me to send you the topic_
            """, parse_mode="markdown")
        else:
            bot.send_message(message.from_user.id, "<b>Here it is the topic that you requested:<b>"
            "*Title:* " + topic_rss['entries'][0]['title'] + "<br>" +
            "*Category:* " + topic_rss['entries'][0]['category'] + "<br>" +
            "*Author:* " + topic_rss['entries'][0]['author'] + "<br><br>" +
            topic_rss['entries'][0]['content'] + "<br><br><br>" +
            "_See it <a href='"+ topic_rss['entries'][0]['link'] + "'>here</a>"
            , parse_mode="html")

###################################################################   RSS COMMANDS

# Handle /latest
@bot.message_handler(commands=['latest'])
def latest_topic(message):
    latest_message = message.text
    latest_get = latest_message.replace('/latest ','')
    # Sends error if missing argument
    if latest_get is None:
        bot.reply_to(message, "*Error: Missing information* - Please send me again the command using this method: `/latest <topic/post>`. If you need more help, send me the command /help", parse_mode="markdown")
    # If not
    else:
        # Handle /latest topic
        if latest_get == "topic":
            rss_url = feedparser.parse(rss_topics_feed)
            message_to_send = "*This is the latest public topic in the " + FORUM_NAME + "*\n\n" + "*Title:* " + rss_url['entries'][0]['title'] + "\n" + "*Category:* " + rss_url['entries'][0]['category'] + "\n" + "*Author:* " + rss_url['entries'][0]['author'] + "\n\n" + "_See it _[here](" + rss_url['entries'][0]['link'] + ")"
            # Sends the content of the topic in a pm
            if message.chat.type != "private":
                message_to_send = message_to_send + "\n\n\nI've also sent you the content of the first message of the topic in a Private Message to prevent flooding. _Remember to start me in Private_"
                bot.reply_to(message, message_to_send, parse_mode="markdown")
            else:
                bot.reply_to(message, message_to_send, parse_mode="markdown")
        # Handle /latest post
        elif latest_get == "post":
            rss_url = feedparser.parse(rss_posts_feed)
            message_to_send = """*This is the latest public post in the """ + FORUM_NAME + """*\n\n""" + "*Main topic:* " + rss_url['entries'][0]['title'] + "\n" + "*Author:* " + rss_url['entries'][0]['author'] + "\n\n" + "_See it _[here](" + rss_url['entries'][0]['link'] + ")"
            # Sends the content of the post in a pm
            if message.chat.type != "private":
                message_to_send = message_to_send + "\n\n\nI've also sent you the content of the post in a Private Message to prevent flooding. _Remember to start me in Private_"
                bot.reply_to(message, message_to_send, parse_mode="markdown")
            else:
                bot.reply_to(message, message_to_send, parse_mode="markdown")
        # Handle /latest number for sending the latest 'number' of topics
        elif hasNumbers(latest_get):
            latest_get_number = latest_get
            rss_url = feedparser.parse(rss_topics_feed)
            # If not in a pm, sends it
            if message.chat.type != "private":
                bot.reply_to(message, "*I've sent you the latest topics in a Private Message*\n_Remember to start me in your account to allow me to send you the message_", parse_mode="markdown")
                counter = 0
                message_to_send = "*The latest " + latest_get + " topics in  " + FORUM_NAME + " are* _(ordered from newest to oldest)_*:*\n\n\n"
                list_topics = ""
                while True:
                    list_topics = list_topics + "*ID:* " + rss_url['entries'][counter]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][counter]['title'] + "](" + rss_url['entries'][counter]['link'] + ")\n\n"
                    counter = counter + 1
                    if counter >= int(latest_get_number):
                        bot.send_message(message.from_user, message_to_send + list_topics, parse_mode="markdown")
                        break
            else:
                counter = 0
                message_to_send = "*The latest " + latest_get_number + " topics in  " + FORUM_NAME + " are* _(ordered from newest to oldest)_*:*\n\n\n"
                list_topics = ""
                while True:
                    list_topics = list_topics + "*ID:* " + rss_url['entries'][counter]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][counter]['title'] + "](" + rss_url['entries'][counter]['link'] + ")\n\n"
                    counter = counter + 1
                    if counter >= int(latest_get_number):
                        bot.reply_to(message, message_to_send + list_topics, parse_mode="markdown")
                        break
        else:
            bot.reply_to(message, "*Error - Unrecognized request* - Please, checkout the command /help to get a complete list of supported commands", parse_mode="markdown")

@bot.message_handler(commands=['test'])
def command_help(message):
    markup = types.InlineKeyboardMarkup()
    itembtna = types.InlineKeyboardButton('a', switch_inline_query="")
    itembtnv = types.InlineKeyboardButton('v', switch_inline_query="")
    itembtnc = types.InlineKeyboardButton('c', switch_inline_query="")
    markup.row(itembtna)
    markup.row(itembtnv, itembtnc)
    bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

###################################################################   MANAGER

# Start the bot
print("Bot ON")
bot.polling()

# Close the bot
print("Bot OFF")
#db.close()
