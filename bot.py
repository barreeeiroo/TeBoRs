import telebot # Bot API Library
from telebot import types # Bot types API library
import time # Library for the time
import feedparser # Imports the feed reader
import threading # Library for the counter
from tinydb import TinyDB, where # Library for the database

###################################################################

#Declare the token
API_TOKEN = '310239734:AAH5AEFwvGMVTUZzohzYmUHZUnpTrvdTw0Q'

# Makes the bot
bot = telebot.TeleBot(API_TOKEN)

# Get the RSS
rss_url = feedparser.parse('http://community.thunkable.com/latest.rss')
last_post = rss_url['entries'][0]['id'].replace("community.thunkable.com-topic-","")

# Declares the database
db = TinyDB('feed.json') # Use this database
table = db.table('rss-feed') # Use this table
#int(latest_post_offline) = table.search(where ('latest_post') > 1)
#print(latest_post_offline, a)
#table.insert({'latest_post': last_post})

#def check_community_feed():
#    threading.Timer(60.0, check_community_feed).start()
#    last_post_online = rss_url['entries'][0]['id']
#check_community_feed()

###################################################################

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
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I the Official Bot of the [Thunkable Community](http://community.thunkable.com).
Check what I can do using the command /help!\
""", parse_mode="markdown")

# Handle '/latest_post'
@bot.message_handler(commands=['latest_post', 'latest_topic'])
def latest_post(message):
    bot.reply_to(message, """*This is the latest public post in the community*\n\n""" +
    "*Title:* " + rss_url['entries'][0]['title'] + "\n" +
    "*Category:* " + rss_url['entries'][0]['category'] + "\n" +
    "*Author:* " + rss_url['entries'][0]['author'] + "\n\n" +
    "_See it _[here](" + rss_url['entries'][0]['link'] + ")",
    parse_mode="markdown")

#Handle /ping
@bot.message_handler(commands=['ping'])
def update_rss(message):
    bot.reply_to(message, "*p*_o_`n`g", parse_mode="markdown")

###################################################################

# Start the bot
bot.polling()
