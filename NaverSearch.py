# -*- coding: utf-8 -*-
import os
import sys
import urllib.request
from http.client import HTTPSConnection
from bs4 import BeautifulSoup as bs

conn = None
client_id = 'xLNuUi5YIoKlaW3aytaj'
client_secret = 'HjY8OAmwmM'

#네이버 OpenAPI 접속 정보 information
server = 'openapi.naver.com'
searchkwrd = ''
encText = ''

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
    print(parsedxml)
    result = parsedxml.find_all('item')
    for item in result:
        title = item.find('title')
        description = item.find('description')
        telephone = item.find('telephone')
        address = item.find('address')
        mapx, mapy = item.find('mapx'), item.find('mapy')
        print(title)
        print(description)
        print(telephone)
        print(address)
        if len(title.text) > 0:
            elements.append({'title': title.text, 'description': description.text, 'telephone': telephone.text,
                             'address': address.text, 'mapx': mapx.text, 'mapy': mapy.text})
    elements = deleteTags(elements)
    return elements

def deleteTags(set):
    for item in set:
        item['title'] = item['title'].replace('<b>', '')
        item['title'] = item['title'].replace('</b>',  '')
    return set

def getLocalDataFromKeyword(keyword):
    global server, conn, client_id, client_secret
    if conn == None:
        connectOPpenApiServer()
    url = userURLBuilder('/v1/search/local.xml',display='10',start='1',query=encText)
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
    return datalist

while True:
    searchkwrd = input('키워드 입력 : ')
    encText = urllib.parse.quote(searchkwrd)
    datalist= getLocalDataFromKeyword(encText)
    print()
    print(datalist)
