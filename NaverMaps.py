import os
import sys
import urllib.request
from http.client import HTTPSConnection
from PIL import Image as Img
from PIL import ImageTk
from io import BytesIO

from tkinter import *

#values
conn = None
client_id = 'zcm64uebro'
client_secret = 'Xfz9zRHcqSuvlCko2ggLQw3FoOYVYNRIOpMOrrxW'
server = 'https://naveropenapi.apigw.ntruss.com'
CRS = 'NHN:128'
Height = 300
Width = 300
LEVEL = 16
#values


def userURLBuilder(url,**user):
    str = url + '?'
    for key in user.keys():
        str += key + '=' + user[key] + '&'
    return str


def connectOPpenApiServer():
    global conn, server
    conn = HTTPSConnection(server)
    conn.set_debuglevel(1)


def getMapDataFromCoordinate(x, y):
    coordinate = str(mapx) + ',' + str(mapy)
    global server, conn, client_id, client_secret, CRS, Height, Width, LEVEL
    url = userURLBuilder('https://naveropenapi.apigw.ntruss.com/map-static/v2/raster', crs=CRS, h=str(Height), w=str(Width),
                         level=str(LEVEL), center=coordinate)
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


mapx = 310269
mapy = 551875
dataimg = getMapDataFromCoordinate(mapx, mapy)
window = Tk()

img = Img.open(BytesIO(dataimg))
image = ImageTk.PhotoImage(img)
label = Label(window, image=image)
label.pack()

window.mainloop()