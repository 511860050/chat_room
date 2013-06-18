#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: test.py
#Date: 2013年 06月 12日 星期三 16:15:52 CST
#Author: chenhuan
#============================================

from Tkinter import *
import tkMessageBox

class PopUp():
  def __init__(self, root, value):
    self.root = root

    self.frame = Frame(root, width=100, height=100)
    self.frame.propagate(False)
    self.frame.pack()

    self.value = StringVar()

    label = Label(self.frame, text='receiver\'s name')
    label.pack()

    entry = Entry(self.frame, textvariable=self.value)
    entry.pack()

    button = Button(self.frame, text='enter', 
                    command=lambda:self.callback(value))
    button.pack()
    
    self.root.mainloop()

  #所有的操作都在这个函数中完成
  def callback(self, value):
    self.value.set('jianghong')
    print self.value.get()


#=======================================================
class Gui():
  def __init__(self, root):
    self.root = root
    self.root.geometry('100x100')

    self.value = []

    button_1 = Button(root, text='pop_up',bg='yellow',
               command=lambda:self.callback_1())
    button_1.pack(expand='yes')

    button_2 = Button(root, text='show', bg='green',
                      command=lambda:self.callback_2())
    button_2.pack(expand='yes')


  def callback_1(self):
    self.popUp = Tk()
    PopUp(self.popUp, self.value)

  def callback_2(self):
    tkMessageBox.showinfo(message='value : %s' % str(self.value))

root = Tk()
gui = Gui(root)
root.mainloop()
