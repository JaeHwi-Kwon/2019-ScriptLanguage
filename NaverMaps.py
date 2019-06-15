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

# tkinter img value
label = None
imgpart = []
img = None
display = None

#command value
x, y = 0, 0
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

def getMapDataFromCoordinate(x, y,isMarker):
    coordinate = str(x) + ',' + str(y)
    marker = SetNMapMarker(x, y)
    global server, conn, client_id, client_secret, CRS, Height, Width, LEVEL
    if isMarker:
        url = userURLBuilder('https://naveropenapi.apigw.ntruss.com/map-static/v2/raster', crs=CRS, h=str(Height),
                             w=str(Width), level=str(LEVEL), center=coordinate, markers=marker)
    else:
        url = userURLBuilder('https://naveropenapi.apigw.ntruss.com/map-static/v2/raster', crs=CRS, h=str(Height),
                             w=str(Width), level=str(LEVEL), center=coordinate)
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


def combineMapImg(imglist):

    return img


def NMapRender(x, y):
    global label, img, imgpart

    imgpart = []

    for i in range(3):
        for j in range(3):
            tempX, tempY = x - DIFF*(1-j), y + DIFF*(1-i)
            dataimg = getMapDataFromCoordinate(tempX, tempY, False)
            if i == 1 and j == 1:
                dataimg = getMapDataFromCoordinate(tempX, tempY, True)
            imgpart.append(Img.open(BytesIO(dataimg)))
            with open("./img/map" + str(i*3+j) + ".png", 'wb') as f:
                f.write(dataimg)
    print("이미지 병합중")
    del(img)
    img = Img.new('RGB', (2100, 2100))
    for i in range(3):
        for j in range(3):
            img.paste(im=imgpart[i*3+j], box=(700*j + (9*i), 700*i - (7*j)))
    img.save("./img/MAP.png")
    display = img.crop((700, 700, 1400, 1400))

    NMapimage = ImageTk.PhotoImage(img)
    label.image = NMapimage
    label.configure(image=NMapimage)
    print("지도 갱신 완료")

def NMapInit(frameName):
    global label, img, mapx, mapy
    #초기값은 산기대

    label = Label(frameName, width=Width, height=Height)
    label.place(x=0, y=0)

    NMapRender(mapx, mapy)



    label.bind_all("<Up>", Keyboard)
    label.bind_all("<Down>", Keyboard)
    label.bind_all("<Left>", Keyboard)
    label.bind_all("<Right>", Keyboard)
    label.bind("<B1-Motion>", MouesMovement)
    label.bind("<ButtonRelease-1>", UpdateMap)

def Keyboard(event):
    print("Keyboard Func has Called!")
    global x, y
    if event.keysym == 'Down':
        pass
    elif event.keysym == 'Up' and y > 0:
        pass
    elif event.keysym == 'Right':
        pass
    elif event.keysym == 'Left' and x > 0:
        pass


def UpdateMap(event):
    global x, y
    NMapRender(x, y)

def MouesMovement(event):
    global x, y, old_event
    print("Mouse Func has Called!")


    old_event = event

#mapx = 310269
#mapy = 551875
#dataimg = getMapDataFromCoordinate(mapx, mapy)
#window = Tk()

#img = Img.open(BytesIO(dataimg))
#image = ImageTk.PhotoImage(img)
#label = Label(window, image=image)
#label.pack()

#window.mainloop()