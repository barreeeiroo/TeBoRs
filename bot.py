#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot # Bot API Library
from telebot import types # Bot types API library
import time # Library for the time
import feedparser # Imports the feed reader
import threading # Library for the counter
import sqlite3 # Library for the database
import sys # Import system libraries
from config import * # Imports the config file

###################################################################

# Encode Emojis
reload(sys)
sys.setdefaultencoding("utf-8")

# Makes the bot
bot = telebot.TeleBot(API_TOKEN)

#Listener
def listener(messages):
    for m in messages:
        cid = m.chat.id
        uid = m.from_user.id
        if m.content_type == 'text': # Sólo saldrán en el log los mensajes tipo texto
            if cid > 0:
                mensaje = "\"" + str(m.from_user.first_name) + " " + str(m.from_user.last_name) + "\" [" + str(cid) + "] -> " + m.text
            else:
                mensaje = "\"" + str(m.from_user.first_name) + " " + str(m.from_user.last_name) + "\" [" + str(cid) + "] -> " + m.text
            f = open('log.txt', 'a')
            f.write(mensaje + "\n")
            f.close()
            print(mensaje)
bot.set_update_listener(listener)

# Feed Updates
conn = sqlite3.connect(DATABASE)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS latest_topic (id int);")

def update_rss():
    #threading.Timer(60.0, update_rss).start()
    rss_url = feedparser.parse(rss_feed)
    latest_post_online = rss_url['entries'][0]['id']
    latest_post_online_id = latest_post_online.replace(FORUM_URL + "-topic-", "")
    print(latest_post_online_id)
    #latest_post_offline = db.execute("SELECT MAX(id) FROM latest_topic;")
    #print(latest_post_offline.fetchone())
#    if latest_post_online > latest_post_offline:
#       db.execute("INSERT INTO latest_topic (id) VALUES (" + latest_post_online + ")")
#       conn.commit()
#       send_updates()
update_rss()

###################################################################

# Handle '/start'
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """\
Hi there, I the Official Bot of the [""" + FORUM_NAME + "](" + FORUM_URL + """).
Check what I can do using the command /help!\
""", parse_mode="markdown")

# Handle /latest_topic
@bot.message_handler(commands=['latest_topic'])
def latest_topic(message):
    rss_url = feedparser.parse(rss_feed)
    bot.reply_to(message, """*This is the latest public post in the """ + FORUM_NAME + """*\n\n""" +
    "*Title:* " + rss_url['entries'][0]['title'] + "\n" +
    "*Category:* " + rss_url['entries'][0]['category'] + "\n" +
    "*Author:* " + rss_url['entries'][0]['author'] + "\n\n" +
    "_See it _[here](" + rss_url['entries'][0]['link'] + ")",
    parse_mode="markdown")

# Handle /latest_post
@bot.message_handler(commands=['latest_post'])
def latest_post(message):
    bot.reply_to(message, """
I am working on this command, sorry
But you can use /latest\_topic to get the latest conversation in the forum
    """,
    parse_mode="markdown")

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

*This is what I can actually do:*
/start - _Starts me_
/help - _This command xD_
/latest\_topic - _Gives you the latest topic in the community_
*Future funcitons:*
- I will notify in """ + GROUP_NAME + """ when a new topic is released in the forum
- You will be able to read any topic from Telegram

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

# Handle /latest
@bot.message_handler(commands=['latest'])
def latest(message):
    if message.chat.type != "private":
        bot.reply_to(message, """
*I've sent you the latest topics in a Private Message*
_Remember to start me in your account to allow me to send you the topic_
        """, parse_mode="markdown")
        rss_url = feedparser.parse(rss_feed)
        bot.send_message(message.from_user.id, "*The latest 10 topics in  " + FORUM_NAME + " are* _(ordered from newest to oldest)_*:*\n\n\n"
        "*ID:* " + rss_url['entries'][0]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][0]['title'] + "](" + rss_url['entries'][0]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][1]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][1]['title'] + "](" + rss_url['entries'][1]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][2]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][2]['title'] + "](" + rss_url['entries'][2]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][3]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][3]['title'] + "](" + rss_url['entries'][3]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][4]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][4]['title'] + "](" + rss_url['entries'][4]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][5]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][5]['title'] + "](" + rss_url['entries'][5]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][6]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][6]['title'] + "](" + rss_url['entries'][6]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][7]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][7]['title'] + "](" + rss_url['entries'][7]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][8]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][8]['title'] + "](" + rss_url['entries'][8]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][9]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][9]['title'] + "](" + rss_url['entries'][9]['link'],
        parse_mode="markdown")
    else:
        rss_url = feedparser.parse(rss_feed)
        bot.reply_to(message, "*The latest 10 topics in  " + FORUM_NAME + " are* _(ordered from newest to oldest)_*:*\n\n\n"
        "*ID:* " + rss_url['entries'][0]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][0]['title'] + "](" + rss_url['entries'][0]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][1]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][1]['title'] + "](" + rss_url['entries'][1]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][2]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][2]['title'] + "](" + rss_url['entries'][2]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][3]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][3]['title'] + "](" + rss_url['entries'][3]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][4]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][4]['title'] + "](" + rss_url['entries'][4]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][5]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][5]['title'] + "](" + rss_url['entries'][5]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][6]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][6]['title'] + "](" + rss_url['entries'][6]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][7]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][7]['title'] + "](" + rss_url['entries'][7]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][8]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][8]['title'] + "](" + rss_url['entries'][8]['link'] + ")\n\n" +
        "*ID:* " + rss_url['entries'][9]['id'].replace(FORUM_URL + "-topic-", "") + " - *Title:* [" + rss_url['entries'][9]['title'] + "](" + rss_url['entries'][9]['link'],
        parse_mode="markdown")

# Send forum update
#def send_updates():
#    bot.send_message(GROUP_ID, "*New post in the community:* \n\n"
#"*Title:* " + rss_url['entries'][0]['title'] + "\n" +
#"*Category:* " + rss_url['entries'][0]['category'] + "\n" +
#"*Author:* " + rss_url['entries'][0]['author'] + "\n\n" +
#"_See it _[here](" + FORUM_URL + "/t/" + latest_post_online + ")",
#    parse_mode="markdown")

###################################################################

# Start the bot
bot.polling()