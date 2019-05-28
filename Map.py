from tkinter import *
from PIL import Image, ImageTk


##################

scale = 4   # 1- 4단계
x, y = 0, 0 # 피봇위치
s = None
img = None

def InitMapPage(frame):
    global s, img
    s = Image.open("Linemap.jpg")
    s1 = s.resize((600,500))
    seoulmap = ImageTk.PhotoImage(s1)
    img = Label(frame, width=450,height=450)
    img.image = seoulmap
    img.configure(image=seoulmap)
    img.place(x=0,y=0)

    img.bind_all("<Key>", move)

    Button(frame, text=' + ', command=sizeUp).pack(side=RIGHT, anchor='s')
    Button(frame, text=' - ', command=sizeDown).pack(side=RIGHT, anchor='s')

def UpdateMapPage():
    global img
    s1 = s.resize((2400//scale, 2000//scale))
    s1 = s1.crop((x,y,x+450,y+450))
    seoulmap = ImageTk.PhotoImage(s1)
    img.image = seoulmap
    img.configure(image=seoulmap)
    print(scale, x, y)


def sizeDown():
    global scale
    scale = min(scale +1, 4)
    UpdateMapPage()

def sizeUp():
    global scale
    scale = max(scale - 1, 1)
    UpdateMapPage()

def move(e):
    global x, y
    if e.keysym == 'Down':
        y = min(y+20, 2000//scale - 450)
    elif e.keysym == 'Up' and y > 0:
        y -= 20
    elif e.keysym == 'Right':
        x = min(x+20, 2400//scale - 450)
    elif e.keysym == 'Left' and x > 0:
        x -= 20
    UpdateMapPage()