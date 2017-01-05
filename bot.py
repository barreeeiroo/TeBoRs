#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot # Bot API Library
from telebot import types # Bot types API library
import time # Library for the time
import feedparser # Imports the feed reader
import threading # Library for the counter
import sqlite3 # Library for the database

###################################################################

#Declare the Token
API_TOKEN = '310239734:AAH5AEFwvGMVTUZzohzYmUHZUnpTrvdTw0Q'

# Declare the main group
GROUP_ID = "1057152889"

#Declare the Forum
FORUM_URL = "community.thunkable.com"

# Declare the Feed
rss_feed = ("http://" + FORUM_URL + '/latest.rss')

# Declares the Database
DATABASE = "feed.db"

###################################################################

#conn = sqlite3.connect(DATABASE)
#db = conn.cursor()
#db.execute("CREATE TABLE IF NOT EXISTS latest_topic (id int);")
#conn.commit()

#def update_rss():
#    threading.Timer(60.0, update_rss).start()
#    latest_post_online = rss_url['entries'][0]['id'].replace(FORUM_URL + "-topic-", "")
#    print(int(latest_post_online)
#    latest_post_offline = db.execute("SELECT MAX(id) FROM latest_topic;")
#    print(latest_post_offline.fetchone())
#    if latest_post_online > latest_post_offline:
#       db.execute("INSERT INTO latest_topic (id) VALUES (" + latest_post_online + ")")
#       conn.commit()
#       send_updates()
#update_rss()

###################################################################

# Makes the bot
bot = telebot.TeleBot(API_TOKEN)

#Listener
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            cid = m.chat.id
            print("[{}]: {}".format(cid, m.text))

bot.set_update_listener(listener)

###################################################################

# Handle '/start'
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """\
Hi there, I the Official Bot of the [Thunkable Community](http://community.thunkable.com).
Check what I can do using the command /help!\
""", parse_mode="markdown")

# Handle /latest_topic
@bot.message_handler(commands=['latest_topic'])
def latest_topic(message):
    rss_url = feedparser.parse(rss_feed)
    bot.reply_to(message, """*This is the latest public post in the community*\n\n""" +
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
But you can use /latest\_topic to get the latest conversation in the community
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
I'm the *official bot of the* [Thunkable Community](http://community.thunkable.com). I'm here to help you in Telegram to use this community

*This is what I can actually do:*
/start - _Starts me_
/help - _This command xD_
/latest\_topic - _Gives you the latest topic in the community_
*Future funcitons:*
- I will notify in @ThunkableGroup when a new topic is released in the community
- You will be able to read any topic from Telegram

Any question, just contact to *my creator*: @barreeeiroo
    """, parse_mode="markdown")

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
