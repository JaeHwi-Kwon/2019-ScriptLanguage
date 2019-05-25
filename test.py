# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from urllib.request import urlopen,Request
from urllib.parse import quote_plus
from xml.etree import ElementTree

import TimeTable

import http.client


class App:

    def __init__(self):
        win = Tk()
        win.geometry("800x600")
        win.resizable(False, False)

        #전체 틀 초기화
        Tap = ttk.Notebook(win, width=500,height=600)
        Tap.pack(side=RIGHT)
        frameLeft = Frame(win)
        frameLeft.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
        frameSearch = Frame(frameLeft,borderwidth=5, relief=RIDGE)
        frameList = Frame(frameLeft,borderwidth=5, relief=RIDGE)
        frameSearch.pack(side=TOP, fill=BOTH)
        frameList.pack(side=BOTTOM)
        frameMap = Frame(win, borderwidth=5, relief=RIDGE)
        framePlase = Frame(win, borderwidth=5, relief=RIDGE)
        frameTime = Frame(win, borderwidth=5, relief=RIDGE)
        Tap.add(frameMap, text='    지도    ')
        Tap.add(framePlase, text='  주변검색  ')
        Tap.add(frameTime, text='   시간표   ')


        #왼쪽 프레임
        self.input = Entry(frameSearch, width=30)
        self.input.pack(side=LEFT)
        self.input.bind('<Return>', self.Search)
        Button(frameSearch,text='검색',command=self.Search).pack()
        scrollbar = Scrollbar(frameList)
        self.listBox = Listbox(frameList,selectmode='extended', width=40,height=20,yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT,fill=BOTH)
        self.listBox.pack(side=LEFT)
        self.listBox.bind('<Double-Button-1>',self.SelectList)
        scrollbar.config(command=self.listBox.yview)


        #오른쪽 프레임
        #시간표
        self.timebox = Text(frameTime)
        self.timebox.pack(fill=BOTH)


        self.stationList = []


        win.mainloop()

    def Search(self, event=None):   #역이름 검색
        keyword = self.input.get()
        key = 'e20GlP6AHkpkkdAr0AYT50r6zfv%2Fgj8KNbomL7RzhiSCSxpFb0vhZgYU7DADHoto16Zxg7xK01%2BCd69yoAssag%3D%3D'
        url = 'http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getKwrdFndSubwaySttnList'
        queryParams = '?' + 'ServiceKey='+ key +'&subwayStationName=' + quote_plus(keyword)

        req = Request(url+queryParams)
        req.get_method = lambda: 'GET'
        res_body = urlopen(req).read()
        print(res_body)
        dataTree = ElementTree.fromstring(res_body)


        self.listBox.delete(0, END)
        namelist = dataTree.getiterator('item')
        for item in namelist:
            name = item.findtext('subwayStationName')
            id = item.findtext('subwayStationId')
            self.listBox.insert(END, name)
            self.stationList.append((name,id))

    def SelectList(self, event):    #목록 더블클릭 했을때
        a = self.listBox.curselection()[0]
        print(self.stationList[a])
        #여기다 오른쪽 탭 갱신하는 함수 호출하면 돼
        self.Updata_Timetable()


    def Updata_Timetable(self):
        table = TimeTable.GetTimeTable(self.stationList[self.listBox.curselection()[0]][1],'01','U')

        self.timebox.delete(1.0,END)
        for i in table:
            self.timebox.insert(END,i+'\n')


App()