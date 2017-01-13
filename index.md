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

## What is this bot for
This bot has been made for helping Discourse users in Telegram to read and be notified for topics in a community
You will be able to read any topic or post from the bot, and even to reply anonymously (working on this function)

---

## Installation
If you want to install the bot, you will need a VPS (VirtualPrivateServer) or a CloudService like [Cloud9](https://c9.io) for hosting it
It works on Linux, Windows or MAC OS

## Prequisites
For been able to run the bot, you will have to install this packages in your system:
- Git
- Python3
- feedparser
- MySQLdb

#### Linux OS
##### Debian or Ubuntu based Distros
If you are on Ubuntu or Debian-based systems, execute these commands:

```bash
sudo apt-get install git
sudo apt-get install python3
sudo apt-get install python-mysqldb
pip3 install feedparser
```

##### CentOS based Distros
If you are on CentOS or based distros, execute these commands:

```bash
sudo yum install git
sudo yum install python3
sudo yum install python-mysqldb
pip3 install feedparser
```

#### Windows
If you are on Windows OS, you will have to download Python3, Git and MySQLDB installers manually from these links:

 - [Git Installer](https://git-scm.com/download/win)
 - [Python3 Installer](https://www.python.org/downloads/windows/)
 - [MySQLDB Installer](http://stackoverflow.com/questions/21440230/install-mysql-python-windows): Follow that small tutorial
 
Aftet that, execute this command in CMD with Administrator Permissions: `pip install feedparser`
