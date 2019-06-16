# -*- coding: utf-8 -*-
#!/usr/bin/python
# coding=utf-8

import sys
import time
import telepot
from pprint import pprint
from datetime import date
import traceback
import TimeTable
import NaverSearch
import NaverMaps
from urllib import parse
from PIL import Image
from requests import *
from io import BytesIO
isSearching = []
tempSearchResult = {}

TOKEN = '801539784:AAFhdzIg3gdWALMfdLWQoclKv-JMr8l2jEo'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)


class IsSearching:
    def __init__(self, user):
        self.id = user
        self.isSearching = False

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)


def sendPhoto(user,img):
    try:
        bot.sendPhoto(user, img)
    except:
        traceback.print_exc(file=sys.stdout)


def replyData(station, user, day):
    print(user, station)
    res_list = TimeTable.GetTimeTableAll(TimeTable.changeToID(station), TimeTable.d[day])
    msg = ''
    for r in res_list:
        if len(r+msg)+1>MAX_MSG_LENGTH:
            sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        sendMessage( user, msg )
    else:
        sendMessage( user, '해당하는 데이터가 없습니다.')


def NSearchTelegram(user, keyword):
    global tempSearchResult
    keyword = parse.quote(keyword)
    facilities = NaverSearch.getLocalDataFromKeyword(keyword)
    tempSearchResult[user] = facilities
    reply = ''
    cnt = 1
    for data in facilities:
        reply += '[' + str(cnt) + '] '
        reply += data['title'] + '\n'
        reply += data['description'] + '\n'
        reply += data['telephone'] + '\n'
        reply += data['address']
        sendMessage(user, reply)
        reply = ''
        cnt += 1
    reply = '지도를 표시하고 싶은 시설의 번호를 적어주십시오'
    sendMessage(user, reply)


def NMapTelegram(user, num):
    global tempSearchResult
    x, y = tempSearchResult[user][num]['mapx'], tempSearchResult[user][num]['mapy']
    dataimg = NaverMaps.getMapDataFromCoordinate(x, y, x, y)
    mapimg = Image.open(BytesIO(dataimg))
    with open("./img/telemap.png", 'wb') as f:
        f.write(dataimg)
    sendPhoto(user, open("./img/telemap.png", 'rb'))

def handle(msg):
    global tempSearchResult
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '텍스트가 아닙니다.')
        return
    text = msg['text']
    args = text.split(' ')
    if chat_id in tempSearchResult:
        if text.startswith('취소'):
            del tempSearchResult[chat_id]
            return
        NMapTelegram(chat_id, int(text))
        del tempSearchResult[chat_id]
        return
    if text.startswith('시간표') and len(args) > 1:
        print('시간표', args[1])
        replyData(args[1], chat_id, args[2])
    elif text.startswith('지역검색') and len(args) > 1:
        NSearchTelegram(chat_id, args[1])
    else:
        sendMessage(chat_id, '모르는 명령어입니다.\n시간표 [역명] [평일] [요일]')


if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print('[', today, ']received token :', TOKEN)

    bot = telepot.Bot(TOKEN)
    pprint(bot.getMe())

    bot.message_loop(handle)

    print('Listening...')

    while 1:
        time.sleep(10)
