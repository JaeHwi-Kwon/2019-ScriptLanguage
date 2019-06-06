# -*- coding: utf-8 -*-

from urllib.request import urlopen,Request
from urllib.parse import quote_plus
from xml.etree import ElementTree

from tkinter import *
from tkinter import ttk
from tkinter.font import *



###############
timebox = None  #시간표 텍스트 상자
daysbox = None  #요일 선택
waybox = None   #방향 선택

page = 0        #보는 페이지
now_station = None  #선택한 역
total = 0       #시간표 개수
dataTree = None     #데이터

mailadd = None  #메일주소 입력창
lastmail = None #메일주소

d = {'평일':'01', '토요일':'02', '일요일':'03'}
w = {'상행':'U', '하행':'D'}
mails = ['@gmail.com','@naver.com','@daum.net']

###############

def GetTimeTable(ID, day, way):
    global total, dataTree

    table = []

    if total == 0:
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

        total = int(dataTree.find("body").findtext('totalCount'))
        print(total)

    list = dataTree.getiterator('item')


    x = 0
    for item in list:
        if x == 0:
            table.append(item.findtext('endSubwayStationNm') + ' 행')
            table.append('')
        if x > page * 25 and x < (page + 1) * 25:
            time = item.findtext('depTime')
            table.append(time)
        x+=1

    return table

def initTimeTable(frame):
    global timebox, daysbox, waybox
    font = Font(family='맑은 고딕', size=12, weight='bold')

    Button(frame, text='이메일로 보내기', font=font, command=MailWindow).pack(side=RIGHT)

    buttonframe = Frame(frame)
    buttonframe.pack(side=BOTTOM)
    Button(buttonframe, width=5, text='->', font=font,bg='DarkOrange1', command=PageUp).pack(side=RIGHT,fill=BOTH)
    Button(buttonframe, width=5, text='<-', font=font,bg='DarkOrange1', command=PageDown).pack(fill=BOTH)
    timebox = Text(frame, state='disabled', width=50, height=28)
    timebox.pack(side=BOTTOM)


    v = ['평일', '토요일', '일요일']
    daysbox = ttk.Combobox(frame,font=font, values=v, width=7, state='readonly')
    daysbox.place(x=100, y=20)
    daysbox.current(0)
    v = ['상행', '하행']
    waybox = ttk.Combobox(frame,font=font, values=v, width=7, state='readonly')
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
    if page < total//25:
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
    mailadd = Entry(win, width=20)
    mailadd.pack(side=LEFT)
    lastmail = ttk.Combobox(win, width=10, values=mails, state='readonly')
    lastmail.pack(side=LEFT)
    lastmail.current(0)

def SendMail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import tkinter.messagebox

    fromadd = 'teyrunia@gmail.com'
    toadd = mailadd.get() + lastmail.get()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = now_station + 'timetable'
    msg['To'] = toadd
    msg['From'] = fromadd

    txt = timebox.get(1.0, END)
    tablePart = MIMEText(txt, 'plain', _charset='UTF-8')
    msg.attach(tablePart)

    try:
        s = smtplib.SMTP('smtp.gmail.com', '587')
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(fromadd, 'sc897799')
        s.sendmail(fromadd, [toadd], msg.as_string())
        s.close()
        tkinter.messagebox.showinfo('전송 성공', '메일을 성공적으로 보냈습니다')
    except BaseException as e:
        tkinter.messagebox.showerror('전송 실패','메일을 보내는데 실패하였습니다')


def GetTimeTableAll(ID, day):
    global total, dataTree

    table = []

    key = 'e20GlP6AHkpkkdAr0AYT50r6zfv%2Fgj8KNbomL7RzhiSCSxpFb0vhZgYU7DADHoto16Zxg7xK01%2BCd69yoAssag%3D%3D'
    url = 'http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getSubwaySttnAcctoSchdulList' + '?ServiceKey=' + key + '&subwayStationId=' + quote_plus(ID) + '&dailyTypeCode=' + quote_plus(day)
    queryParams ='&upDownTypeCode=' + quote_plus('U')
    queryParams +='&pageNo=' + '1' + '&numOfRows=' + '300'

    req = Request(url + queryParams)
    req.get_method = lambda: 'GET'
    res_body = urlopen(req).read()
    print(res_body)
    dataTree = ElementTree.fromstring(res_body)


    ulist = dataTree.getiterator('item')

    queryParams = '&upDownTypeCode=' + quote_plus('D')
    queryParams += '&pageNo=' + '1' + '&numOfRows=' + '300'

    req = Request(url + queryParams)
    req.get_method = lambda: 'GET'
    res_body = urlopen(req).read()
    print(res_body)
    dataTree = ElementTree.fromstring(res_body)

    dlist = dataTree.getiterator('item')

    x = 0
    for i, j in zip(ulist, dlist):
        if x == 0:
            table.append(i.findtext('endSubwayStationNm') + ' 행' + '    ' + j.findtext('endSubwayStationNm') + '행')
            table.append('')
        else:
            time = i.findtext('depTime') +'     '+ j.findtext('depTime')
            table.append(time)
        x+=1

    return table

def changeToID(name):
    key = 'e20GlP6AHkpkkdAr0AYT50r6zfv%2Fgj8KNbomL7RzhiSCSxpFb0vhZgYU7DADHoto16Zxg7xK01%2BCd69yoAssag%3D%3D'
    url = 'http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getKwrdFndSubwaySttnList'
    queryParams = '?' + 'ServiceKey=' + key + '&subwayStationName=' + quote_plus(name)

    req = Request(url + queryParams)
    req.get_method = lambda: 'GET'
    res_body = urlopen(req).read()
    print(res_body)
    dataTree = ElementTree.fromstring(res_body)

    namelist = dataTree.getiterator('item')
    id = ''
    for item in namelist:
        id = item.findtext('subwayStationId')
        break
    return id


if __name__ == '__main__':
    GetTimeTable('SUB214', '01', 'U')