from tkinter import *
from tkinter import filedialog
import os
from PIL import ImageTk, Image

# style
root = Tk()
root.title('Youtube Playlist Into Spreadsheet')
root.geometry('800x600')
root.resizable(False, False)
mfont = ('Georgia', 15)
sfont = ('Georgia', 13)
xsfont = ('Georgia', 12)

# image
pic = ImageTk.PhotoImage(Image.open('image.png'))
label1 = Label(image=pic)
label1.pack(side=LEFT)

# contents
main = PanedWindow(root, background='#f1f1f1')
main.pack(side=RIGHT, fill=BOTH, expand=True)

# entry bars
apitxt = Label(main, text='API Key', font=mfont, background='#f1f1f1')
apibox = Entry(main, bd=2, font=sfont)
apitxt.pack(side=TOP, anchor=NW, pady=(20, 2), padx=30)
apibox.pack(side=TOP, fill=X, padx=30)

plid = Label(main, text='Playlist ID', font=mfont, background='#f1f1f1')
plbox = Entry(main, bd=2, font=sfont)
plid.pack(side=TOP, anchor=NW, pady=(17, 5), padx=30)
plbox.pack(side=TOP, fill=X, padx=30)


# directory
def askdir():
    dirname = filedialog.askdirectory()
    if dirname:
        dirpath.set(dirname)


dirpath = StringVar(root)
dirpath.set(os.path.dirname(os.path.realpath(__file__)))

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
c4but = Checkbutton(cframe, text='Upload Date', command=lambda: list_toggle('Upload Date'), font=xsfont)
c5but = Checkbutton(cframe, text='Description', command=lambda: list_toggle('Description'), font=xsfont)
c1but.grid(row=0, column=0, sticky=W, padx=(70, 30))
c2but.grid(row=1, column=0, sticky=W, padx=(70, 30))
c3but.grid(row=0, column=1, sticky=W, padx=(60, 0))
c4but.grid(row=1, column=1, sticky=W, padx=(60, 0))
c5but.grid(row=2, column=1, sticky=W, padx=(60, 0))

# end buttons
savebut = Button(main, text="Save Settings", width=15, font=xsfont)
exportbut = Button(main, text="Export Sheet", width=15, font=xsfont)
savebut.pack(side=LEFT, padx=(60, 0))
exportbut.pack(side=RIGHT, padx=(0, 60))
