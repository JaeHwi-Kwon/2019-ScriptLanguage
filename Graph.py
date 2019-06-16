# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.font import *
from tkinter import ttk
from urllib.request import urlopen,Request
from urllib.parse import quote_plus
from xml.etree import ElementTree



h = 4
v = ['1호선','2호선','3호선','4호선','5호선']
data = None
canvas = None

def initGraph(frame):
    global canvas
    canvas = Canvas(frame,width=600,height=500, bg='white')
    canvas.pack()
    bframe = Frame(frame,bg='black')
    bframe.pack( fill='x')
    line = ttk.Combobox(bframe, values=v,state='readonly')
    line.current(0)
    line.grid(row=0, column=0, padx=50)
    Button(bframe, text=" < ", command=prebutton).grid(row=0, column=1)
    Button(bframe, text=" > ", command=nextbutton).grid(row=0, column=2)




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
        data = None
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
    bt = 400
    lt = 100

    for i in range(25):
        x = i*20
        y = 200
        canvas.create_line(x,y,x+20,y)

    pass

def UpdateGraph(line, station):
    getCard(line, station)
    drowGraph()