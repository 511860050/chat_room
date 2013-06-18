#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: test.py
#Date: 2013年 06月 12日 星期三 16:15:52 CST
#Author: chenhuan
#============================================

from Tkinter import *
import tkMessageBox

root = Tk()

frame = Frame(root, width=200, height=100, bg='yellow')
frame.propagate(False)
frame.pack()

valueLabel = StringVar()
valueEntry = StringVar()

def callback(event):
   value = valueEntry.get()
   print 'before:', type(value)
   if str(type(value)) == "<type 'unicode'>" :
     value = value.encode('utf-8')
     print 'after:', type(value)
   value = str(value)
   valueLabel.set(value)
   valueEntry.set('')

label = Entry(frame, textvariable=valueLabel, bg='green')
label.pack(expand='yes')

entry = Entry(frame, textvariable=valueEntry)
entry.bind('<Key-Return>', callback)
entry.pack(expand='yes')

root.mainloop()

