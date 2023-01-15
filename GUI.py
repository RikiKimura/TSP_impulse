from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import subprocess
import time

root = Tk()
style = ttk.Style()
style.configure('.', font = ('', 18))

root.title('TSP測定スクリプト')



frame1 = ttk.Frame(root, padding=10)
frame1.grid()

title1 = ttk.Label(frame1, text='TSPインパルス応答測定', font=("",30),padding=(0, 20))
title1.grid(row=0, column=0, columnspan=3)

label1 = ttk.Label(frame1, text='・名前', padding=(5, 2), anchor='w', justify='left', font=("",18))
label1.grid(row=1, column=0, sticky=W)

label2 = ttk.Label(frame1, text='・信号長2^? (ex:15)', padding=(5, 2), anchor='w', justify='left', font=("",18))
label2.grid(row=2, column=0, sticky=W)

label3 = ttk.Label(frame1, text='・加算平均回数 (ex:5)', padding=(5, 2), anchor='w', justify='left', font=("",18))
label3.grid(row=3, column=0, sticky=W)

label4 = ttk.Label(frame1, text='・測定回数 (ex:10)', padding=(5, 2), anchor='w', justify='left', font=("",18))
label4.grid(row=4, column=0, sticky=W)

label5 = ttk.Label(frame1, text='・サンプルレート (ex:44100)', padding=(5, 2), anchor='w', justify='left', font=("",18))
label5.grid(row=5, column=0, sticky=W)

label6 = ttk.Label(frame1, text='・チャンネル数 (ex:2)    ', padding=(5, 2), anchor='w', justify='left', font=("",18))
label6.grid(row=6, column=0, sticky=W)

label7 = ttk.Label(frame1, text='・入力デバイス番号 (ex:12)', padding=(5, 2), anchor='w', justify='left', font=("",18))
label7.grid(row=7, column=0, sticky=W)

label7 = ttk.Label(frame1, text='・出力デバイス番号 (ex:13)', padding=(5, 2), anchor='w', justify='left', font=("",18))
label7.grid(row=8, column=0, sticky=W)

# Username Entry
username = StringVar()
username_entry = ttk.Entry(
    frame1,
    textvariable=username,
    width=25,
    font=("",18))
username_entry.grid(row=1, column=1, columnspan=2)

# siganal length
signallength = StringVar()
signallength_entry = ttk.Entry(
    frame1,
    textvariable=signallength,
    width=25,
    font=("",18))
signallength_entry.grid(row=2, column=1, columnspan=2)

# sync addition time
syncadd = StringVar()
syncadd_entry = ttk.Entry(
    frame1,
    textvariable=syncadd,
    width=25,
    font=("",18))
syncadd_entry.grid(row=3, column=1, columnspan=2)

# measurement times
meatimes = StringVar()
meatimes_entry = ttk.Entry(
    frame1,
    textvariable=meatimes,
    width=25,
    font=("",18))
meatimes_entry.grid(row=4, column=1, columnspan=2)

# sample rate
samplerate = StringVar()
samplerate_entry = ttk.Entry(
    frame1,
    textvariable=samplerate,
    width=25,
    font=("",18))
samplerate_entry.grid(row=5, column=1, columnspan=2)
samplerate_entry.insert(0,"44100")

# Radiobutton 1
v1 = StringVar()
rb1 = ttk.Radiobutton(
    frame1,
    text='1',
    value='1',
    variable=v1,
    width=8)

# Radiobutton 2
rb2 = ttk.Radiobutton(
    frame1,
    text='2',
    value='2',
    variable=v1,
    width=8)

rb1.grid(row=6, column=1)# LabelFrame
rb2.grid(row=6, column=2)

# inputdevice
devicein = StringVar()
devicein_entry = ttk.Entry(
    frame1,
    textvariable=devicein,
    width=25,
    font=("",18))
devicein_entry.grid(row=7, column=1, columnspan=2)

# outputdevice
deviceout = StringVar()
deviceout_entry = ttk.Entry(
    frame1,
    textvariable=deviceout,
    width=25,
    font=("",18))
deviceout_entry.grid(row=8, column=1, columnspan=2)


button = ttk.Button(
    frame1, text='デバイス番号確認',
    command=lambda: [txt.delete("1.0","end"), txt.insert(1.0, subprocess.check_output(['python', 'devicelist.py']).decode("utf8"))])
button.grid(row=9, column=0, columnspan=2)

readme = ttk.Button(
    frame1, text='Readme',
    command=lambda: [txt.delete("1.0","end"), txt.insert(1.0, subprocess.check_output(['type', 'readme.txt'],shell=True).decode("utf8"))])
readme.grid(row=9, column=1, columnspan=2)

clearbutton = ttk.Button(
    frame1, text='Clear',
    command=lambda: [username_entry.delete(0,"end"), signallength_entry.delete(0,"end"), syncadd_entry.delete(0,"end"), meatimes_entry.delete(0,"end"), samplerate_entry.delete(0,"end"), devicein_entry.delete(0,"end"), deviceout_entry.delete(0,"end"), txt.delete("1.0","end")])
clearbutton.grid(row=9, column=2, columnspan=2)


button1 = ttk.Button(
    frame1, text='測定開始',
    command=lambda: [txt.delete("1.0","end"), subprocess.Popen(['start', 'python', 'TSP_impulse.py',
                                                               username_entry.get(), signallength_entry.get(),
                                                               syncadd_entry.get(), meatimes_entry.get(),
                                                               samplerate_entry.get(), v1.get(), devicein_entry.get(),
                                                               deviceout_entry.get()], shell=True)])
button1.grid(row=10, column=0, columnspan=2)

button2 = ttk.Button(frame1, text='Exit', command=quit)
button2.grid(row=10, column=1, columnspan=2)


# Text
f = Font(family='Helvetica', size=14)
v2 = StringVar()
txt = Text(frame1, height=12, width=85)
txt.configure(font=f)
txt.grid(row=11, column=0, columnspan=3)

# Scrollbar
scrollbar = ttk.Scrollbar(
    frame1,
    orient=VERTICAL,
    command=txt.yview)
txt["yscrollcommand"] = scrollbar.set
scrollbar.grid(row=11, column=3)

root.mainloop()
