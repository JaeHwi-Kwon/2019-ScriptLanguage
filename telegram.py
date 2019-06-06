#!/usr/bin/python
# coding=utf-8

import sys
import time
import telepot
from pprint import pprint
from datetime import date
import traceback
import TimeTable


TOKEN = '896070727:AAEKXdR-S5c5I8MwCmta7__5cdAIrbdW-vA'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
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
        sendMessage( user, '해당하는 데이터가 없습니다.' )

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '텍스트가 아닙니다.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('시간표') and len(args)>1:
        print('시간표', args[1])
        replyData(args[1], chat_id, args[2] )
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