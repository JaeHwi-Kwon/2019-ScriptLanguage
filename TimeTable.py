# -*- coding: utf-8 -*-

from urllib.request import urlopen,Request
from urllib.parse import quote_plus
from xml.etree import ElementTree

from tkinter import *
from tkinter.ttk import *


###############
timebox = None  #시간표 텍스트 상자
daysbox = None  #요일 선택
waybox = None   #방향 선택

d = {'평일':'01', '토요일':'02', '일요일':'03'}
w = {'상행':'U', '하행':'D'}

###############

def GetTimeTable(ID, day, way):
    key = 'e20GlP6AHkpkkdAr0AYT50r6zfv%2Fgj8KNbomL7RzhiSCSxpFb0vhZgYU7DADHoto16Zxg7xK01%2BCd69yoAssag%3D%3D'
    url = 'http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getSubwaySttnAcctoSchdulList'
    queryParams = '?' + 'ServiceKey=' + key + '&subwayStationId=' + quote_plus(ID)
    queryParams +='&dailyTypeCode=' + quote_plus(day)
    queryParams +='&upDownTypeCode=' + quote_plus(way)
    queryParams +='&pageNo=' + '1'
    queryParams +='&numOfRows=' + '300'

    req = Request(url + queryParams)
    req.get_method = lambda: 'GET'
    res_body = urlopen(req).read()
    print(res_body)
    dataTree = ElementTree.fromstring(res_body)

    table = []

    list = dataTree.getiterator('item')
    for item in list:
        time = item.findtext('depTime')
        table.append(time)

    return table


def initTimeTable(frame):
    global timebox, daysbox, waybox

    timebox = Text(frame, state='disabled')
    timebox.pack(side=BOTTOM)

    v = ['평일', '토요일', '일요일']
    daysbox = Combobox(frame, values=v, width=7, state='readonly')
    daysbox.place(x=100, y=20)
    daysbox.current(0)
    v = ['상행', '하행']
    waybox = Combobox(frame, values=v, width=7, state='readonly')
    waybox.place(x=200, y=20)
    waybox.current(0)





def UpdateTimeTable(frame, station):
    global timebox

    table = GetTimeTable(station, d[daysbox.get()], w[waybox.get()])

    timebox['state'] = 'normal'

    timebox.delete(1.0, END)
    for i in table:
        timebox.insert(END, i + '\n')

    timebox['state'] = 'disable'




if __name__ == '__main__':
    GetTimeTable('SUB214', '01', 'U')