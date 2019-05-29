import os
import sys
import urllib.request
from http.client import HTTPSConnection
from PIL import Image as Img
from PIL import ImageTk
from io import BytesIO

from tkinter import *

#values start
conn = None
client_id = 'zcm64uebro'
client_secret = 'Xfz9zRHcqSuvlCko2ggLQw3FoOYVYNRIOpMOrrxW'
CRS = 'NHN:128'
Height = 550
Width = 485
LEVEL = 14
label = []
#values end


def userURLBuilder(url,**user):
    str = url + '?'
    for key in user.keys():
        str += key + '=' + user[key] + '&'
    return str


def SetNMapMarker(x, y):
    marker = 'type:d|size:mid|pos:' + str(x) + '%20' + str(y)
    return marker

def getMapDataFromCoordinate(x, y):
    coordinate = str(x) + ',' + str(y)
    marker = SetNMapMarker(x,y)
    global server, conn, client_id, client_secret, CRS, Height, Width, LEVEL
    url = userURLBuilder('https://naveropenapi.apigw.ntruss.com/map-static/v2/raster', crs=CRS, h=str(Height), w=str(Width),
                         level=str(LEVEL), center=coordinate, markers=marker)
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        print('Map data download complete!')
        response_body = response.read()
        return response_body

    else:
        print('Error Code' + rescode)
        return None


def NMapRender(x,y):
    global label
    mapx, mapy = x,y
    dataimg = getMapDataFromCoordinate(mapx, mapy)
    img = Img.open(BytesIO(dataimg))
    NMapimage = ImageTk.PhotoImage(img)
    label.image = NMapimage
    label.configure(image=NMapimage)

def NMapInit(frameName):
    global label
    #초기값은 산기대
    mapx = 287975
    mapy = 527209
    dataimg = getMapDataFromCoordinate(mapx, mapy)
    img = Img.open(BytesIO(dataimg))
    NMapimage = ImageTk.PhotoImage(img)
    label = Label(frameName,width=Width,height=Height)
    label.image = NMapimage
    label.configure(image=NMapimage)
    label.place(x=0, y=0)

#mapx = 310269
#mapy = 551875
#dataimg = getMapDataFromCoordinate(mapx, mapy)
#window = Tk()

#img = Img.open(BytesIO(dataimg))
#image = ImageTk.PhotoImage(img)
#label = Label(window, image=image)
#label.pack()

#window.mainloop()