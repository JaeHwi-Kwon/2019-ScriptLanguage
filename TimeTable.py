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

page = 0        #보는 페이지
now_station = None  #선택한 역

mailadd = None  #메일주소 입력창
lastmail = None #메일주소

d = {'평일':'01', '토요일':'02', '일요일':'03'}
w = {'상행':'U', '하행':'D'}
mails = ['@gmail.com','@maver.com','@daum.net']

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
    x = 0
    for item in list:
        if x > page * 30 and x < (page + 1) * 30:
            time = item.findtext('depTime')
            table.append(time)
        x+=1

    return table


def initTimeTable(frame):
    global timebox, daysbox, waybox

    Button(frame, text='이메일로 보내기', command=MailWindow).pack(side=RIGHT)

    buttonframe = Frame(frame)
    buttonframe.pack(side=BOTTOM)
    Button(buttonframe, width=5, text='->', command=PageUp).pack(side=RIGHT,fill=BOTH)
    Button(buttonframe, width=5, text='<-', command=PageDown).pack(fill=BOTH)
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




def UpdateTimeTable(station):
    global timebox, now_station
    now_station = station
    table = GetTimeTable(station, d[daysbox.get()], w[waybox.get()])

    timebox['state'] = 'normal'

    timebox.delete(1.0, END)

    for i in table:
        timebox.insert(END, i + '\n')


    timebox['state'] = 'disable'

def PageUp():
    global page
    page += 1
    UpdateTimeTable(now_station)

def PageDown():
    global page
    if page > 1:
        page -= 1
    UpdateTimeTable(now_station)

def MailWindow():
    global mailadd, lastmail

    win = Tk()
    win.geometry("300x100")
    win.resizable(False, False)

    Label(win, text='이메일 주소').pack(fill=BOTH)
    Button(win, text='시간표 보내기', command=SendMail).pack(side=BOTTOM)
    mailadd = Entry(win, width=15)
    mailadd.pack(side=LEFT)
    lastmail = Combobox(win, width=10, values=mails)
    lastmail.pack(side=LEFT)

def SendMail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    msg = MIMEMultipart('alternative')
    msg['Subject'] = now_station + '시간표입니다'
    msg['To'] = mailadd.get() + lastmail.get()
    msg['From'] = 'teyrunia@gmail.com'





if __name__ == '__main__':
    GetTimeTable('SUB214', '01', 'U')