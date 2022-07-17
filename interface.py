from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox import askyesno
import sys
import os
from PIL import ImageTk, Image


# set path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# style
root = Tk()
root.title('Youtube Playlist Into Spreadsheet')
root.geometry('850x570')
root.iconbitmap(default=resource_path('icon.ico'))
root.resizable(False, False)
mfont = ('Georgia', 15)
sfont = ('Georgia', 13)
xsfont = ('Georgia', 12)

# image
pic = ImageTk.PhotoImage(Image.open(resource_path('image.png')))
label1 = Label(image=pic)
label1.pack(side=LEFT)

# contents
main = PanedWindow(root, background='#f1f1f1')
main.pack(side=RIGHT, fill=BOTH, expand=True)

# entry bars
apifield = StringVar(root)
apitxt = Label(main, text='API Key', font=mfont, background='#f1f1f1')
apibox = Entry(main, bd=2, textvariable=apifield, font=sfont)
apitxt.pack(side=TOP, anchor=NW, pady=(20, 2), padx=30)
apibox.pack(side=TOP, fill=X, padx=30)

plfield = StringVar(root)
plid = Label(main, text='Playlist ID', font=mfont, background='#f1f1f1')
plbox = Entry(main, bd=2, textvariable=plfield, font=sfont)
plid.pack(side=TOP, anchor=NW, pady=(17, 5), padx=30)
plbox.pack(side=TOP, fill=X, padx=30)


# directory
def askdir():
    dirname = filedialog.askdirectory()
    if dirname:
        dirpath.set(dirname)


dirpath = StringVar(root)
dirframe = Frame(main, background='#f1f1f1')
dirlabel = Label(main, text='Export To', font=mfont, background='#f1f1f1')
dirlabel.pack(side=TOP, anchor=NW, pady=(17, 5), padx=30)
getdir = Button(dirframe, text=' ... ', command=askdir)
getdir.pack(side=RIGHT, anchor=NE)
w = Entry(dirframe, bd=2, font=sfont, textvariable=dirpath, state='disabled')
w.pack(side=TOP, anchor=NE, fill=X)
dirframe.pack(side=TOP, fill=X, padx=30)


# listbox
def moveup():
    try:
        lboxcurse = lbox.curselection()
        if not lboxcurse:
            return
        for pos in lboxcurse:
            if pos == 0:
                continue
            text = lbox.get(pos)
            lbox.delete(pos)
            lbox.insert(pos - 1, text)
            lbox.selection_set(pos - 1)
            lbox.activate(pos - 1)
    except:
        pass


def movedown():
    try:
        lboxcurse = lbox.curselection()
        if not lboxcurse:
            return
        for pos in lboxcurse:
            if pos == lbox.size() - 1:
                continue
            text = lbox.get(pos)
            lbox.delete(pos)
            lbox.insert(pos + 1, text)
            lbox.selection_set(pos + 1)
            lbox.activate(pos - 1)
    except:
        pass


lframe = Frame(main, background='#f1f1f1')
lframe.pack(side=TOP, fill=X, padx=30, pady=20)
moveupbutton = Button(lframe, text="Move Up", command=moveup, width=12, font=xsfont)
movedownbutton = Button(lframe, text="Move Down", command=movedown, width=12, font=xsfont)
lbox = Listbox(lframe, font=sfont, height=6)
lbox.pack(side=RIGHT, fill=X, padx=5)
moveupbutton.pack(pady=(30, 0))
movedownbutton.pack(pady=25)

# checklist
cframe = Frame(main, background='#f1f1f1')
cframe.pack(side=TOP, fill=X, padx=30)


def list_toggle(item):
    if item in lbox.get(0, "end"):
        pos = lbox.get(0, "end").index(item)
        lbox.delete(pos)
    else:
        lbox.insert(END, item)


c1but = Checkbutton(cframe, text='Title', command=lambda: list_toggle('Title'), font=xsfont)
c2but = Checkbutton(cframe, text='URL', command=lambda: list_toggle('URL'), font=xsfont)
c3but = Checkbutton(cframe, text='Uploader', command=lambda: list_toggle('Uploader'), font=xsfont)
c4but = Checkbutton(cframe, text='Date', command=lambda: list_toggle('Date'), font=xsfont)
c5but = Checkbutton(cframe, text='Description', command=lambda: list_toggle('Description'), font=xsfont)
c1but.grid(row=0, column=0, sticky=W, padx=(40, 0))
c2but.grid(row=1, column=0, sticky=W, padx=(40, 0))
c3but.grid(row=0, column=1, sticky=W, padx=(40, 0))
c4but.grid(row=1, column=1, sticky=W, padx=(40, 0))
c5but.grid(row=0, column=3, sticky=W, padx=(15, 0))

# end buttons
savebut = Button(main, text="Save Settings", width=15, font=xsfont)
exportbut = Button(main, text="Export Sheet", width=15, font=xsfont)
savebut.pack(side=LEFT, padx=(60, 0))
exportbut.pack(side=RIGHT, padx=(0, 60))
