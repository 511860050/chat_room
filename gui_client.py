#!/usr/bin/python 
# -*- coding: utf-8 -*-
#============================================
#FileName: client_gui.py
#Date: 2013年 06月 09日 星期日 20:58:15 CST
#Author: chenhuan
#Usage: the GUI of chat_client
#============================================

from Tkinter import *
import tkMessageBox
import tkFileDialog
import socket
import sys
import re
import os
from threading import Thread

def errorMessage(errorInfo):
  tkMessageBox.showerror(message=errorInfo)

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
      prefix = inputText.split(' ', 1)[0]
      if prefix == 'SENDFILE':
        toAddress, fileName = inputText.split(' ')[1:3]
        if self.ifSendFile(toAddress):
          self.show('Send File Begin\n')
          self.sendFile(toAddress, fileName)
          self.show('Send File Over\n')
      elif prefix == 'RECEIVEFILE':
        fromAddress, fileName = inputText.split(' ')[1:3]
        if self.ifRecvFile(fromAddress):
          self.show('Receive File Begin\n')
          self.recvFile(fromAddress, fileName)
          self.show('Receive File Over\n')
      elif inputText == 'UPDATE NAMES':
        self.updateNames()  
      elif re.search(r'Your nickname is .+', inputText):
        self.client.nickname=re.search(r'Your nickname is (.+)',
                                       inputText).group(1)
        self.show(inputText+'\n')
        self.client.updateNames()
      else:
        self.show(inputText+'\n')

  def ifSendFile(self, toAddress):
    """
    ifSendFile - acording to the response from toAddress to deside 
    weather to send file
    Return True = receive 'YES'
    Return False = receive 'NO'
    """
    line = self.client.readFd.readline().strip()
    try:
      name,line = line.split(' ', 1)
    except: line = ''
    if name == '<'+toAddress+'>' and line == 'YES':
      return True
    return False

  def ifRecvFile(self, fromAddress):
    msg ='A file will be send from %s\n receive it or not?' % fromAddress
    recvFlag = tkMessageBox.askquestion(message=msg)
    if recvFlag == 'yes':
      self.client.writeFd.write('/%s YES\n' % fromAddress)
      return True
    elif recvFlag == 'no':
      self.client.writeFd.write('/%s NO\n' % fromAddress)
      return False

  def sendFile(self, toAddress, fileName):
    try:
      fd = open(fileName, 'rb')
    except:
      errroMessage("Error in open %s" % fileName)
      return

    while True:
      line = fd.readline()
      if line:
        message = "/%s %s" % (toAddress, line)
        self.client.writeFd.write(message)
      else: break
    message = "/%s %s\n" % (toAddress, 'SENDFILEOVER')
    self.client.writeFd.write(message)

  def recvFile(self, fromAddress, fileName):
    """
    RecvFile - receive the file as 'fileName' from fromAddress
    store the file in './download' as "fromAddress_fileName"
    """
    path = './download/%s_%s' % (fromAddress, fileName)
    try:
      fd = open(path, 'wb')
    except:
      tkMessageBox.showerror('Error in open %s' % path) 
    firstFlag = False

    while True:
      line = self.client.readFd.readline()
      #the first line is a empty unuse line
      if not firstFlag:
        firstFlag = True
        continue
      #keep the empty line
      try:
        line = line.split(' ', 1)[1]
      except:
        line = '\n'
      #The binary format file may not be ended by '\n'
      #so the 'SENDFILEOVER\n' may be added to the tail of the 
      #last line, so checking if the line is ended by 'SENDFILEOVER\n' 
      #is more reasonable
      endPattern = re.compile(r'SENDFILEOVER\n$')
      if not endPattern.search(line):
        fd.write(line)
      else: 
        if line == 'SENDFILEOVER\n': 
          pass
        else:
          otherPart = re.compile(r'(.+)SENDFILEOVER\n$')
          line = otherPart.match(line).group(1)
          fd.write(line)
        break
    fd.close()
    
  def updateNames(self):
    userList = self.client.userList

    userList.delete('0.0', 'end') #clear the userList
    while True:
      inputText = self.client.readFd.readline().strip() 
      if inputText != 'UPDATE NAMES OVER':
        if inputText == self.client.nickname:
          #make my nickname differenct
          begin = userList.index('insert')
          userList.insert('end', inputText+'\n')
          userList.see('end')
          end = userList.index('insert')

          userList.tag_add('myName', begin, end)
          userList.tag_config('myName', background='blue')
        else:
          userList.insert('end', inputText+'\n')
      else : break

  def show(self, message):
    outputWidget = self.client.outputWidget

    pattern = re.compile(r'^<.+>.*')
    if pattern.match(message):
      outputWidget.insert('end', message)
      outputWidget.see('end')
    else:
      #set the system message to be 'red'
      begin = outputWidget.index('insert')
      outputWidget.insert('end', message)
      outputWidget.see('end')
      end = outputWidget.index('insert')

      outputWidget.tag_add('systemMessage', begin, end)
      outputWidget.tag_config('systemMessage', foreground='red')

#=======================================================
class LoginGui():
  """
  LoginGui - create the gui of Log in 
  """
  def __init__(self, root):
    self.root = root
    self.address = StringVar()

    self.createWidget()

  def connectToServer(self, serverAddr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serverAddr, port))
    self.readFd = sock.makefile('rb', 0)
    self.writeFd = sock.makefile('wb', 0)

  def createWidget(self):
    frame = Frame(self.root, width=250, height=500, bg='yellow')
    frame.propagate(False)
    frame.pack()

    widgetFrame = Frame(frame, bg='yellow')
    widgetFrame.pack(expand='yes')

    addrInfo = Label(widgetFrame, text='Fromat: ip_address:port', 
                     bg='yellow')
    addrInfo.pack(expand='yes')

    addrEntry = Entry(widgetFrame, textvariable=self.address)
    addrEntry.focus_set()
    addrEntry.bind('<KeyPress-Return>', self.callback)
    addrEntry.pack(expand='yes')

    button = Button(widgetFrame, text='Log in', 
                    command=lambda:self.enterFunc())
    button.pack(expand='yes')

  def enterFunc(self):
    line = self.address.get().strip()
    parts = line.split(':')
    if re.match(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$', parts[0].strip()):
      serverAddr = parts[0]
    else:
      self.address.set('')
      errorMessage('Unvalid IP address!\nTry again!')
      return
    if re.match(r'[0-9]+', parts[1].strip()):
      port = int(parts[1])
    else:
      self.address.set('')
      errorMessage('Unvalide port number!\nTry again!')
      return

    try:
      self.connectToServer(serverAddr, port)
      self.root.destroy()
    except :
      self.address.set('')
      errorMessage('Unable to connect to server!\nTry again!')
      return

  def callback(self, event):
    self.enterFunc()

#=======================================================
class SendFileGui(Toplevel):
  """
  RecvNameGui - read the recvName to send the file to
  """
  def __init__(self, chatClient, fileName):
    Toplevel.__init__(self)

    self.chatClient = chatClient
    self.fileName = fileName
    self.recvName = StringVar()

    label = Label(self, text='Receiver\'s name')
    label.pack()

    entry = Entry(self, textvariable=self.recvName)
    entry.pack()

    button = Button(self, text='Enter', command=lambda:self.callback())
    button.pack()

  def callback(self):
    print 'Here you are'
    recvName = self.recvName.get()
    #to process the Chinese
    if str(type(recvName)) == "<type 'unicode'>":
      recvName = recvName.encode('utf-8')
    self.chatClient.writeFd.write("/file %s %s\n" % 
                                 (recvName, self.fileName))
    self.destroy()

#=======================================================
class ChatGui(Frame):
  """
  ChatGui - create the gui of ChatClient
  """
  def __init__(self, chatClient):
    Frame.__init__(self, width=500, height=400, bg='green')
    self.propagate(False)
    self.pack()

    self.chatClient = chatClient
    self.inputText = StringVar()
    self.createWidget()

  def fileFunc(self):
    fileName = tkFileDialog.askopenfilename()
    SendFileGui(self.chatClient, fileName)

  def enterFunc(self):
    line = self.inputText.get().strip()
    if line:
      #to process the Chinese
      if str(type(line)) == "<type 'unicode'>":
        line = line.encode('utf-8')
      self.chatClient.writeFd.write(line+'\n')
    self.inputText.set('')
    
  def callback(self, event):
    self.enterFunc()
      
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
    inputWidget = Entry(leftFrame, textvariable=self.inputText,
                        width=55, takefocus=0)
    inputWidget.bind('<KeyPress-Return>', self.callback)
    inputWidget.focus_set()
    inputWidget.pack(fill='x', pady=2)
    #Enter button
    enterButton = Button(leftFrame, text='Enter',
                        command=(lambda: self.enterFunc()))
    enterButton.pack(anchor='se', side='right', fill='y')
    #File button
    fileButton = Button(leftFrame, text='Send File',
                        command=(lambda: self.fileFunc()))
    fileButton.pack(anchor='sw', side='left', fill='y')
    #user list
    rightFrame = Frame(self, width=100, height=400, bg='yellow')
    rightFrame.propagate(False)
    rightFrame.pack(side='left', padx=4)

    label = Label(rightFrame, text='Users\' List', bg='cyan')
    label.pack(side='top', fill='x')

    self.userList = Text(rightFrame, bg='yellow', fg='red')
    self.userList.pack(expand='yes', fill='both')

#=======================================================
class ChatClient:
  """
  ChatClient - build the connection to Chat_Server
  """
  def __init__(self):
    self.initialGui()

    self.nickname = None
    self.names = []

    #New thread to get input from socket
    socketInput = SocketInput(self)
    socketInput.start()

    self.clientGui.mainloop()

  def initialGui(self):
#    root = Tk() 

#    loginGui = LoginGui(root) 
#    root.mainloop()
#    try:
#      self.readFd = loginGui.readFd
#      self.writeFd = loginGui.writeFd
#    except:
#      sys.exit(-1)

    #------------------------------------------------------- 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('10.12.11.241', 13000))
    self.readFd = sock.makefile('rb', 0)
    self.writeFd = sock.makefile('wb', 0)
    #-------------------------------------------------------

    self.clientGui = ChatGui(self)
    self.outputWidget = self.clientGui.outputWidget
    self.userList = self.clientGui.userList

  def updateNames(self):
    """
    UpdateNames - send '/who' to server, and severve the names
    """
    self.writeFd.write('/who\n')

#======================================================
if __name__ == '__main__':
  ChatClient()
