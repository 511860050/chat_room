#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: client_gui.py
#Date: 2013年 06月 09日 星期日 20:58:15 CST
#Author: chenhuan
#Usage: the GUI of chat_client
#============================================

from Tkinter import *
import socket
import sys
import re
import os
from threading import Thread

#======================================================
class SocketInput(Thread):
  """
  SocketOutput - get the input from socket and send them to the 
  standard output
  """
  def __init__(self, client):
    Thread.__init__(self)
    self.setDaemon(self)
    self.client = client
  
  def run(self):
    while True:
      inputText = self.client.readFd.readline().strip()
      if inputText == 'A FILE WILL BE SEND':
        self.client.outputWidget.insert('end','A file will be send\n')
        self.client.outputWidget.insert('end', \
'---------Receive File Begin-------------\n')
        self.receiveFile()
        self.client.outputWidget.insert('end', \
'----------Receive File Over-------------\n')
      elif inputText == 'UPDATE NAMES':
        self.updateNames()  
      elif re.search(r'Your nickname is [a-zA-Z]+', inputText):
        self.client.nickname=re.search(r'Your nickname is ([a-zA-Z]+)',
                                       inputText).group(1)
        self.client.outputWidget.insert('end', inputText+'\n')
        self.client.outputWidget.see('end')
        self.client.updateNames()
      else:
        print inputText.strip()
        self.client.outputWidget.insert('end', inputText+'\n')
        self.client.outputWidget.see('end')

  def receiveFile(self):
    """
    ReceiveFile - receive the file from other client
    """
    #receive filename
    inputText = self.client.readFd.readline()
    parts = inputText.split(' ')
    print 'parts : ', parts
    if parts[0] == 'filename' :
      fileName = os.path.split(parts[1])[1]
    else:
      print 'Error in receive fileName'
      return
    #receive file 
    fd = open(fileName.strip(), 'w')
    while True:
      inputText = self.client.readFd.readline().strip()
      if inputText != 'SEND FILE OVER':
        fd.write(inputText+'\r\n')
      else: break
    fd.close()

  def updateNames(self):
    self.client.userList.delete('0.0', 'end') #clear the userList
    while True:
      inputText = self.client.readFd.readline().strip() 
      if inputText != 'UPDATE NAMES OVER':
        self.client.userList.insert('end', inputText+'\n')
      else : break

 #=======================================================
class ChatClient:
  """
  Chat_Client - build the connection to Chat_Server
  """
  def __init__(self, serverAddr, port):
    self.initialGui()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serverAddr, port))
    try :
      self.readFd = sock.makefile('rb', 0)
      self.writeFd = sock.makefile('wb', 0)
    except :
      print 'Error in sock.makefile'

    self.nickname = None
    self.names = []

    self.run()
    self.root.mainloop()

  def initialGui(self):
    self.root = Tk() 
    
    self.inputText = StringVar()
    def enterCallback(event):
      self.standardInput()

    leftFrame = Frame(self.root, width=400, height=400, bg='green')
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
    self.inputWidget.bind('<KeyPress-Return>', enterCallback)
    self.inputWidget.focus_set()
    self.inputWidget.pack(fill='x', pady=2)
    #Enter button
    self.enterButton =Button(leftFrame, text='Enter',
                             command=(lambda:self.standardInput()))
    self.enterButton.pack(anchor='se', expand='yes', fill='y')
    #user list
    rightFrame = Frame(self.root, width=100, height=400, bg='yellow')
    rightFrame.propagate(False)
    rightFrame.pack(side='left', padx=4)

    self.userList = Text(rightFrame, bg='yellow', fg='red')
    self.userList.pack(expand='yes', fill='both')

  def standardInput(self):
    inputText = self.inputText.get().strip()
    if inputText:
      self.writeFd.write(inputText+'\r\n')
    self.inputText.set('')

  def updateNames(self):
    """
    UpdateNames - send '/who' to server, and severve the names
    """
    self.writeFd.write('/who\r\n')
    
  def run(self):
    """
    Run - get the inputs from socket and send them to the stdout
    """
    socketInput = SocketInput(self)
    socketInput.start()

#======================================================
if __name__ == '__main__':
  if len(sys.argv) != 3 :
    print 'Usage %s [address] [port]' % sys.argv[0]
    exit(-1)

  ChatClient(sys.argv[1], int(sys.argv[2]))
