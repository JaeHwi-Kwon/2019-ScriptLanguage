# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.font import *
from tkinter import ttk
from urllib.request import urlopen,Request
from urllib.parse import quote_plus
from xml.etree import ElementTree

import cplus

h = 4
v = ['1호선','2호선','3호선','4호선','5호선']
data = []
canvas = None
p = 0

def initGraph(frame):
    global canvas
    canvas = Canvas(frame,height=500, bg='white')
    canvas.pack(fill='x')
    #bframe = Frame(frame,bg='black')
    #bframe.pack( fill='x')
    #line = ttk.Combobox(bframe, values=v,state='readonly')
    #line.current(0)
    #line.grid(row=0, column=0, padx=50)
    #Button(bframe, text=" < ", command=prebutton).grid(row=0, column=1)
    #Button(bframe, text=" > ", command=nextbutton).grid(row=0, column=2)




def getCard(line='4호선',station='정왕역'):
    global data
    key = '655746787474657936305a4861426a'
    url = 'http://openAPI.seoul.go.kr:8088/' +key +'/xml/CardSubwayTime/' + '1/5/' + '201901/' + quote_plus(line+'/'+station) + '/'

    print(url)
    req = Request(url)
    req.get_method = lambda: 'GET'
    res_body = urlopen(req).read()
    print('카드 얻어오기')
    root = ElementTree.fromstring(res_body)
    dataTree = root.find("row")

    data = []
    list = []
    if root.findtext("CODE") != 'INFO-000' and root.findtext('CODE') != None:
        print(root.findtext("CODE"))
        print("데이터 없음")
        data = []
        return

    for i in dataTree.iter():
        list.append(i.text)
    #print(list)
    for i in range(4,51,2):
        data.append(eval(list[i])+eval(list[i+1]))
    print(data)


def prebutton():
    global h
    h = max(h-1, 4)

def nextbutton():
    global h
    h += 1

def drowGraph():
    global p
    if p == 100:
        p=1

    mx = 0
    tp = 50
    bt = 400 +tp
    lt = 100

    canvas.delete('all')

    if len(data) != 0:
        mx = max(data)
        canvas.create_text(lt-30,bt-380, text=str(mx))

    canvas.delete('d')
    per = p/100
    for i in range(23):
        x = i*21 + lt + 30
        if mx != 0:
            cplus.calc(data[i], 380, per, mx)
            y2 = bt - data[i+1]*380*per//mx
            canvas.create_line(x,y,x+21,y2, width=3, fill='SeaGreen3', tag='d')
        canvas.create_text(x,bt+10, text=str((i+4)%25),tag='d')


    canvas.create_line(lt, tp, lt, bt, lt + 520, bt, width=7, arrow='both')
    p+=1
    if p <100:
        canvas.after(10, drowGraph)


def UpdateGraph(line, station):
    getCard(line, station)
    drowGraph()