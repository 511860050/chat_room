#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: login_gui.py
#Date: 2013年 06月 15日 星期六 09:35:56 CST
#Author: chenhuan
#Usage: The gui of log in
#============================================

from Tkinter import *

class LoginGui(Frame):
  def __init__(self):
    Frame.__init__(self, width=250, height=500, bg='yellow')
    self.propagate(False)
    self.pack()

    self.createWidget()

  def createWidget(self):
    frame = Frame(self, bg='yellow')
    frame.pack(expand='yes')

    addrInfo = Label(frame, text='Fromat: ip_address port', bg='yellow')
    addrInfo.pack(expand='yes')

    addrEntry = Entry(frame)
    addrEntry.pack(expand='yes')

    button = Button(frame, text='Log in')
    button.pack(expand='yes')

app = LoginGui()
app.mainloop()

