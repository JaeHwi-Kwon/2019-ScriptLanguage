import os
import sys
import urllib.request
from http.client import HTTPSConnection
from PIL import Image as Img
from PIL import ImageTk
from io import BytesIO

from tkinter import *

#values start
# parsing
conn = None
client_id = 'zcm64uebro'
client_secret = 'Xfz9zRHcqSuvlCko2ggLQw3FoOYVYNRIOpMOrrxW'

# map parsing value
CRS = 'NHN:128'
Height = 700
Width = 700
LEVEL = 14
DIFF = 2660
mapx, mapy = 287975, 527209
markx,marky = 287975, 527209

# tkinter img value
label = None
imgpart = []
img = None
display = None

#command value
x, y = 700, 700
old_event = None
#vlues end


def userURLBuilder(url,**user):
    str = url + '?'
    for key in user.keys():
        str += key + '=' + user[key] + '&'
    return str


def SetNMapMarker(x, y):
    marker = 'type:d|size:mid|pos:' + str(x) + '%20' + str(y)
    return marker

def getMapDataFromCoordinate(x, y):
    global server, conn, client_id, client_secret, CRS, Height, Width, LEVEL,markx,marky
    coordinate = str(x) + ',' + str(y)
    marker = SetNMapMarker(markx, marky)
    url = userURLBuilder('https://naveropenapi.apigw.ntruss.com/map-static/v2/raster', crs=CRS, h=str(Height),
                        w=str(Width), level=str(LEVEL), center=coordinate, markers=marker)
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


def NMapRender(x, y):
    global label, img, imgpart,mapx,mapy
    imgpart = []
    mapx,mapy = x,y
    for i in range(3):
        for j in range(3):
            tempX, tempY = x - DIFF*(1-j), y + DIFF*(1-i)
            dataimg = getMapDataFromCoordinate(tempX, tempY)
            if i == 1 and j == 1:
                dataimg = getMapDataFromCoordinate(tempX, tempY)
            imgpart.append(Img.open(BytesIO(dataimg)))
#            with open("./img/map" + str(i*3+j) + ".png", 'wb') as f:
#                f.write(dataimg)
    print("이미지 병합중")
    img = Img.new('RGB', (2100, 2100))
    for i in range(3):
        for j in range(3):
            img.paste(im=imgpart[i*3+j], box=(700*j + (9*i), 700*i - (7*j)))
#    img.save("./img/MAP.png")
    display = img.crop((700, 700, 1400, 1400))

    NMapimage = ImageTk.PhotoImage(display)
    label.image = NMapimage
    label.configure(image=NMapimage)
    print("지도 갱신 완료")

def NMapInit(frameName):
    global label, img, mapx, mapy

    label = Label(frameName, width=Width, height=Height)
    label.place(x=0, y=0)

    NMapRender(mapx, mapy)

    label.bind("<B1-Motion>", MouesMovement)
    label.bind("<ButtonRelease-1>", UpdateMap)


def UpdateMap(event):
    global x, y, old_event, mapx, mapy
    mapx += int(((x-700))*DIFF/700)
    mapy -= int(((y-700))*DIFF/700)
    old_event = None
    x, y = 700, 700
    NMapRender(mapx, mapy)

def MouesMovement(event):
    global x, y, old_event
    print("Mouse Func has Called!")
    if old_event != None:
        dx, dy = event.x - old_event.x, event.y - old_event.y
        x = max(0, min(x - dx, 1400))
        y = max(0, min(y - dy, 1400))
    old_event = event
    MovImg()

def MovImg():
    global img, label
    display = img.crop((x, y, x+700, y+700))
    NMapimage = ImageTk.PhotoImage(display)
    label.image = NMapimage
    label.configure(image=NMapimage)


#mapx = 310269
#mapy = 551875
#dataimg = getMapDataFromCoordinate(mapx, mapy)
#window = Tk()

#img = Img.open(BytesIO(dataimg))
#image = ImageTk.PhotoImage(img)
#label = Label(window, image=image)
#label.pack()

#window.mainloop()