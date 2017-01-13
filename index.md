# TeBoRs (for [Discourse Forums](http://discourse.org))
Simple, Useful and OpenSource

---

[![Travis](https://img.shields.io/travis/rust-lang/rust.svg?style=flat-square)](https://github.com/barreeeiroo/TeBoRs)

## Table of Contents

* [What is this bot for](#what-is-this-bot-for)
* [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [Setup](#seup)
  * [Running](#running)
  * [Update](#update)
* [How to use](#how-to-use)
  * [Admin](#admin)
  * [User](#user)
* [Support](#support)
  * [Future Functions](#future-functions)
  * [Issues](#issues)
  * [Credits](#credits)
  
---
---

## What is this bot for
This bot has been made for helping Discourse users in Telegram to read and be notified for topics in a community
You will be able to read any topic or post from the bot, and even to reply anonymously (working on this function)

---

## Installation
If you want to install the bot, you will need a VPS (VirtualPrivateServer) or a CloudService like [Cloud9](https://c9.io) for hosting it
It works on Linux, Windows or MAC OS

### Prequisites
For been able to run the bot, you will have to install this packages in your system:

- Git
- Python3
- MySQL Server
- feedparser
- MySQLdb

#### Linux OS
##### Debian or Ubuntu based Distros
If you are on Ubuntu or Debian-based systems, execute these commands:

```bash
sudo apt-get install git
sudo apt-get install python3
sudo apt-get install mysqld
sudo apt-get install python-mysqldb
pip3 install feedparser
```

##### CentOS based Distros
If you are on CentOS or based distros, execute these commands:

```bash
sudo yum install git
sudo yum install python3
sudo yum install mariadb
sudo yum install python-mysqldb
pip3 install feedparser
```

#### Mac OS
We couldn't test it on Mac OS system, but you can Google for how to install those packages in your OS

#### Windows
If you are on Windows OS, you will have to download Python3, Git and MySQLDB installers manually from these links:

 - [Git Installer](https://git-scm.com/download/win)
 - [Python3 Installer](https://www.python.org/downloads/windows/)
 - For MySQL in Windows you can use [XAMPP Server](https://www.apachefriends.org/)
 - [MySQLDB Installer](http://stackoverflow.com/questions/21440230/install-mysql-python-windows): Follow that small tutorial
 
Aftet that, execute this command in CMD with Administrator Permissions to install feedparser: `pip install feedparser`

---

### Setup
Now it's time to clone the bot and configure it. Clone the repository using this command:

```bash
git clone -b discourse https://github.com/barreeeiroo/TeBoRs
```

When you have succesfully cloned it, open `config.py` file using an editor like _nano_ or _vim_ and change these settings:

- **API_TOKEN** = Setup your own BotFather ApiToken
- **ADMIN_NAME** = Your Telegram Name
- **ADMIN_NICKAME** = Your Telegram Nickname
- **ADMIN_ID** = Your Telegram ID
- **GROUP_NAME** = The main group nickname if it's publick, or the name if it's private
- **GROUP_ID** = The group ID
- **FORUM_NAME** = The name of the Discourse Forum
- **FORUM_PROTOCOL** = The protocol that you are actually using (https or http)
- **FORUM_URL** = The domain for your community
- **DB_NAME** = Your MySQL database
- **DB_HOST** = Your MySQL host (usually `localhost`)
- **DB_USER** = Your MySQL user
- **DB_PASS** = Your MySQL user's password

---

### Running
For running the bot in tests mode, you can simple execute the command

```bash
python3 bot.py
```

But if you want to make the bot running forever, you will have to install the package `screen` for your OS and execute in the terminal

```bash
screen python3 bot.py
```
and with it if you close your screen the bot will be running in the background

---

### Update
To update the bot to the latest version, just run this command in your folder:

```bash
git pull
```

But if you get any error like _Files must be commited_ or similar, then save your config.py file in your HardDrive, delete the folder TeBoRs and clone again and paste your config.py file

---
---

## How to use
This is a part to teach users and admins for how to sue the bot

### Admins
