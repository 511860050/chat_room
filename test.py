#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: test.py
#Date: 2013年 06月 12日 星期三 16:15:52 CST
#Author: chenhuan
#============================================

from Tkinter import *
import tkFileDialog

#=======================================================
class Gui():
  """
  recvnamegui - read the recvname to send the file to
  """
  def __init__(self, root):
    self.root = root
    self.recvName = StringVar()

    b = Button(root, text='Enter', command=lambda:self.func())
    b.pack()

    self.top = Toplevel(self.root)

    label = Label(self.top, text='receiver\'s name')
    label.pack()

    entry = Entry(self.top, textvariable=self.recvName)
    entry.pack()

    button = Button(self.top, text='enter', 
                    command=lambda:self.callback())
    button.pack()

  def func(self):
    print self.recvName.get()

  def callback(self):
    self.recvName.get()
    self.top.destroy()

root = Tk()
gui = Gui(root)
root.mainloop()
