#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: chat_gui.py
#Date: 2013年 06月 15日 星期六 08:56:56 CST
#Author: chenhuan
#Usage: The gui of ChatClient
#============================================

from Tkinter import *

class ChatGui(Frame):
  def __init__(self):
    Frame.__init__(self, chatClient, width=500, height=400, bg='green')
    self.propagate(False)
    self.pack()

    self.chatClient = chatClient
    self.inputText = StringVar()
    self.createWidget()

  def callback(event):
    self.standardInput()

  def standardInput(self):
    line = self.inputText.get().strip()
    if line:
      self.chatClient.writeFd.write(line+'\n')
    self.inputText.set('')
      
  def createWidget(self):
    leftFrame = Frame(self, width=400, height=400, bg='green')
    leftFrame.propagate(False)
    leftFrame.pack(side='left')
    #output Text
    textFrame = Frame(leftFrame, width=400, height=340, bg='red')
    textFrame.propagate(False)
    textFrame.pack()

    self.outputWidget = Text(textFrame)
    self.outputWidget.pack(expand='yes', fill='both')
    #input Entry
    self.inputWidget = Entry(leftFrame, textvariable=self.inputText,
                             width=55, takefocus=0)
    self.inputWidget.bind('<Keypress-Return>', callback)
    self.inputWidget.focus_set()
    self.inputWidget.pack(fill='x', pady=2)
    #Enter button
    self.enterButton =Button(leftFrame, text='Enter',
                             command=(lambda: self.standardInput()))
    self.enterButton.pack(anchor='se', expand='yes', fill='y')
    #user list
    rightFrame = Frame(self, width=100, height=400, bg='yellow')
    rightFrame.propagate(False)
    rightFrame.pack(side='left', padx=4)

    self.userList = Text(rightFrame, bg='yellow', fg='red')
    self.userList.pack(expand='yes', fill='both')
