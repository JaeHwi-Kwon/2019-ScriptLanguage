from tkinter import *
from tkinter.font import *
from PIL import Image, ImageTk


##################

scale = 0   # 1- 7단계
x, y = 0, 0 # 피봇위치
s = None
img = None

def InitMapPage(frame):
    global s, img
    s = Image.open("Linemap.jpg")
    s1 = s.resize((750,700))
    seoulmap = ImageTk.PhotoImage(s1)
    img = Label(frame, width=700-15,height=700-15, bg='white')
    img.image = seoulmap
    img.configure(image=seoulmap)
    img.place(x=0,y=0)

    img.bind_all("<Up>", move)
    img.bind_all("<Down>", move)
    img.bind_all("<Left>", move)
    img.bind_all("<Right>", move)

    buttonfont = Font(family='맑은 고딕', size=12, weight='bold')

    Button(frame, text=' ＋ ',font=buttonfont, bg='DarkOrange1', command=sizeDown).pack(side=RIGHT, anchor='s')
    Button(frame, text=' － ',font=buttonfont, bg='DarkOrange1', command=sizeUp).pack(side=RIGHT, anchor='s')

def UpdateMapPage():
    global img
    s1 = s.resize((720+scale*240, 700+scale*185))
    s1 = s1.crop((x,y,x+700,y+700))
    seoulmap = ImageTk.PhotoImage(s1)
    img.image = seoulmap
    img.configure(image=seoulmap)
    print(scale, x, y)


def sizeDown():
    global scale
    scale = min(scale +1, 7)
    UpdateMapPage()

def sizeUp():
    global scale
    scale = max(scale - 1, 0)
    UpdateMapPage()

def move(e):
    global x, y
    if e.keysym == 'Down':
        y = min(y+20, scale*190)
    elif e.keysym == 'Up' and y > 0:
        y -= 20
    elif e.keysym == 'Right':
        x = min(x+20, scale*230)
    elif e.keysym == 'Left' and x > 0:
        x -= 20
    UpdateMapPage()
