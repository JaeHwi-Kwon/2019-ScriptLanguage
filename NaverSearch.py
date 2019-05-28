# -*- coding: utf-8 -*-
import os
import sys
import urllib.request
from http.client import HTTPSConnection
from bs4 import BeautifulSoup as bs

from tkinter import *


#string values start

conn = None
client_id = 'xLNuUi5YIoKlaW3aytaj'
client_secret = 'HjY8OAmwmM'

server = 'openapi.naver.com'
searchkwrd = ''
encText = ''
#string values end

#tkinter values start
Nsearch = None
NSearchButtons = []
NSearchResultTxt = []
scrollvalue = 0

#tkinter values end


def userURLBuilder(url,**user):
    str = url + '?'
    for key in user.keys():
        str += key + '=' + user[key] + '&'
    return str


def connectOPpenApiServer():
    global conn, server
    conn = HTTPSConnection(server)
    conn.set_debuglevel(1)


def extractwithBS4(strXml):
    elements = []
    parsedxml=bs(strXml,'lxml-xml')
    result = parsedxml.find_all('item')
    for item in result:
        title = item.find('title')
        description = item.find('description')
        telephone = item.find('telephone')
        address = item.find('address')
        mapx, mapy = item.find('mapx'), item.find('mapy')
        if len(title.text) > 0:
            elements.append({'title': title.text, 'description': description.text, 'telephone': telephone.text,
                             'address': address.text, 'mapx': mapx.text, 'mapy': mapy.text})
    elements = deleteTags(elements)
    return elements


def deleteTags(set):
    for item in set:
        item['title'] = item['title'].replace('<b>', '')
        item['title'] = item['title'].replace('</b>',  '')
        item['description'] = item['description'].replace('<b>', '')
        item['description'] = item['description'].replace('</b>',  '')
        item['address'] = item['address'].replace('<b>', '')
        item['address'] = item['address'].replace('</b>', '')
    return set


def getLocalDataFromKeyword(keyword):
    global server, conn, client_id, client_secret
    if conn == None:
        connectOPpenApiServer()
    url = userURLBuilder('/v1/search/local.xml',display='20',start='1',query=keyword)
    conn.request('GET', url, None, {'X-Naver-Client-Id':client_id,'X-Naver-Client-Secret': client_secret})
    req = conn.getresponse()
    print(req.status)
    if int(req.status == 200):
        print('Local data download complete!')
        decoded_data = req.read().decode('utf-8')
        return extractwithBS4(decoded_data)
    else:
        print('Error Code' + req.status)
        return None


def getNaverSearchData(searchkwrd):
    encText = urllib.parse.quote(searchkwrd)
    datalist= getLocalDataFromKeyword(encText)
    print(datalist)
    return datalist


def NSearchInit(frameName):
    global Nsearch, NSearchButtons
    Nsearch = Entry(frameName, width=64)
    Nsearch.grid(row=0, column=0)
    Button(frameName, text='검색', command=NaverSearchfunc).grid(row=0, column=1)
    resultFrame = Frame(frameName, borderwidth=5, relief=RIDGE)
    resultFrame.grid(row=1, column=0)
    for i in range(7):
        NSearchButtons.append(Button(resultFrame, text='', width=62))
        NSearchButtons[i].pack()
    Button(frameName, command=ScrollUp, text='▲').place(x=460, y=200)
    Button(frameName, command=ScrollDown, text='▼').place(x=460, y=300)


def clamp(min,x,max):   #최대, 최소값으로 제한하는 함수
    if x < min:
        return min
    elif x > max:
        return max
    else:
        return x


def ScrollUp():
    global scrollvalue,NSearchResultTxt
    scrollvalue -= 1
    scrollvalue = clamp(0, scrollvalue, 13)
    for i in range(7):
        NSearchButtons[i].configure(text=NSearchResultTxt[i+scrollvalue])


def ScrollDown():
    global scrollvalue, NSearchResultTxt
    scrollvalue += 1
    scrollvalue = clamp(0, scrollvalue, 13)
    for i in range(7):
        NSearchButtons[i].configure(text=NSearchResultTxt[i + scrollvalue])


def NaverSearchfunc():
    global Nsearch, NSearchResultTxt, scrollvalue
    NSearchResultTxt = []
    scrollvalue = 0
    keyword = Nsearch.get()
    searchResult = getNaverSearchData(keyword)
    for i in range(20):
        text = ('이름 : ' + searchResult[i]['title'] +'\n설명 : ' + searchResult[i]['description'] + '\n전화 번호 : '
                + searchResult[i]['telephone'] + '\n주소 : ' + searchResult[i]['address'])
        NSearchResultTxt.append(text)
    for i in range(7):
        NSearchButtons[i].configure(text=NSearchResultTxt[i])


#while True:
#    searchkwrd = input('키워드 입력 : ')
#    datalist= getNaverSearchData(searchkwrd)
#    print()
#    print(datalist)