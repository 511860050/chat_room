#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: client_gui.py
#Date: 2013年 06月 09日 星期日 20:58:15 CST
#Author: chenhuan
#Usage: the GUI of chat_client
#============================================

from Tkinter import *
import chat_client
import socket
import sys
import re
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
    self.readFd = client.readFd
    self.outputWidget = client.outputWidget #control variable
  
  def run(self):
    while True:
      inputText = self.readFd.readline().strip()
      if inputText == 'A FILE WILL BE SEND\r\n':
        print 'A file will be send'
        print '---------Receive File Begin-------------'
        self.receiveFile()
        print '----------Receive File Over-------------'
      elif re.search(r'Your nickname is [a-zA-Z]+', inputText):
        self.client.nickname=re.search(r'Your nickname is ([a-zA-Z]+)',
                                       inputText).group(1)
        self.outputWidget.insert('end', inputText+'\n')
      else:
        print inputText.strip()
        self.outputWidget.insert('end', inputText+'\n')

  def receiveFile(self):
    """
    ReceiveFile - receive the file from other client
    """
    inputText = self.readFd.readline()
    parts = inputText.split(' ')
    if parts[0] == 'filename' :
      fileName = os.path.split(parts[1])[1]
    else:
      print 'Error in receive fileName'
      return
    
    fd = open(fileName.strip(), 'w')
    while True:
      inputText = self.readFd.readline()
      if inputText != 'SEND FILE OVER\r\n':
        fd.write(inputText.strip()+'\r\n')
      else:
        break
    fd.close()

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

    self.run()
    self.win.mainloop()

  def initialGui(self):
    self.win = Frame(None, width=400, height=400)
    self.win.pack_propagate(0)
    self.win.pack()

    self.inputText = StringVar()
    def enterCallback(event):
      self.standardInput()

    self.enterButton =Button(self.win, text='Enter', width=60, height=2, 
                             command=(lambda:self.standardInput()))
    self.enterButton.pack(side=BOTTOM)

    self.inputWidget = Entry(self.win, textvariable=self.inputText,
                             takefocus=0, width=60)
    self.inputWidget.bind('<KeyPress-Return>', enterCallback)
    self.inputWidget.focus_set()
    self.inputWidget.pack(side=BOTTOM)

    self.outputWidget = Text(self.win, width=60, height=21, takefocus=0)
    self.outputWidget.pack(side=TOP)

  def standardInput(self):
    inputText = self.inputText.get().strip()
    if inputText:
      self.writeFd.write(inputText+'\r\n')
      if self.nickname:
         inputText = "<%s> %s" % (self.nickname, inputText)
      self.outputWidget.insert("end", inputText+'\n')
    self.inputText.set('')

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
