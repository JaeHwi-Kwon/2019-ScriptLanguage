# -*- coding: utf-9 -*-
from tkinter import *
from tkinter import ttk
from urllib.parse import urlparse
from urllib.request import urlopen,Request
from urllib.parse import urlencode, quote_plus
from xml.dom.minidom import parseString

import http.client


class App:

    def __init__(self):
        win = Tk()
        win.geometry("800x600")
        win.resizable(False, False)


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



        self.input = Entry(frameSearch, width=30)
        self.input.pack(side=LEFT)
        Button(frameSearch,text='검색',command=self.Search).pack()
        scrollbar = Scrollbar(frameList)
        self.listBox = Listbox(frameList,selectmode='extended', width=40,height=20, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT,fill=BOTH)
        self.listBox.pack(side=LEFT)
        scrollbar.config(command=self.listBox.yview)


        win.mainloop()

    def Search(self):
        sttkwrd = self.input.get()
        url = 'http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getKwrdFndSubwaySttnList'
        queryParams = '?' + urlencode({quote_plus('ServiceKey'): '	yYG2IhrTJ8VGFAjuP8SXOXHnxdu7B9XGBRzAz3Uxn2rNdzpkeyOi85h8hKIbTVo2%2FdjNEQnPWm7Oipb5mxEzEg%3D%3D',
                                       quote_plus('subwayStationName'): sttkwrd})

        req = Request(url+queryParams)
        req.get_method = lambda: 'GET'
        res_body = urlopen(req).read()
        print(res_body)
        xmldata = parseString(res_body)

        self.listBox.delete(0, int(self.listBox.size())-1)

#        list = xmldata.childNodes
#        stations = list[1].childNodes
#        for s in stations:
#            if s.nodeName == 'item':
#                self.listBox.insert(0, s.firstChild.nodeValue)



App()