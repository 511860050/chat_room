#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: chat_server.py
#Date: 2013年 06月 07日 星期五 16:08:35 CST
#Author: chenhuan
#Usage: chat server
#============================================

import asyncore
import socket
import os
from asyncore import dispatcher
from asynchat import async_chat

PORT = 13000

class ChatSession(async_chat) :
  """
  ChatSession - deal with the connection with a client
  """
  def __init__(self, server, sock):
    async_chat.__init__(self, sock)
    self.set_terminator('\r\n')

    self.data = []
    self.server = server
    self.nickname = ""
    self.nameFlag = False

    self.push("Enter you nickname: "+'\r\n')
    
  def isNickname(self):
    """
    isNickname - true = line is nickname
    """
    return self.nameFlag is False

  def getNickname(self, nickname):
    """
    GetNickname - check if the nickname in server.names
    """
    if nickname not in self.server.names:
      self.nickname = nickname
      self.server.names.append(nickname)
      self.nameFlag = True
      self.push('Your nickname is %s\r\n' % nickname)
    else :
      self.push('Name %s is exist, Enter another one: \r\n' % nickname) 

  def isCommand(self, line):
    """
    isCommand - True = line is a command
    command begin with the key word as follows :
    exit - leave the chat room
    who - show the client list
    """
    line = line.strip()
    cmd = line.split(' ', 1)[0]
    if cmd[0] is '/' :
      return True
    return False

  def updateNames(self):
    """
    Do_who - show the online clients
    command format - /who
    """
    self.server.broadcast(self, 'UPDATE NAMES\r\n')
    for name in self.server.names:
      self.server.broadcast(self, name+'\r\n')
    self.server.broadcast(self, 'UPDATE NAMES OVER\r\n')

  def processCommand(self, line):
    """
    ProcessCommand - process the command
    """
    def do_exit(self, msg):
      """
      Do_exit - print the message then exit the chat_server
      command format - /exit
      """
      self.server.broadcast(self,'%s is logout %s\r\n' % \
                           (self.nickname,msg))

    def do_privateChat(self, name, msg):
      """
      Do_privateChat - private chat 
      command format - /nickname message
      """
      for session in self.server.sessions :
        if name == session.nickname :
          message = "<%s> %s" % (self.nickname, msg)
          session.push(message+'\r\n')

    def sendLine(self, name, line):
      """
      SendLine - send line to the pointed client
      """
      if name not in self.server.names:
        self.push('%s not exist\r\n' % name)
        return

      for session in self.server.sessions:
        if name == session.nickname:
          session.push(line+'\r\n')

    def do_file(self, msg):
      """
      Do_file - transport the file to pointed client
      command format - /file [nickname] [filename]
      """
      msg = msg.strip()
      parts = msg.split(' ')
      #get recvName and filename
      recvName = parts[0].strip()
      try :
        fileName = parts[1].strip()
      except IndexError :
        self.push('File format: /file [nickname] [filename]\r\n')
        return

      if recvName in self.server.names :
        #check if file exist
        try:
          os.stat(fileName) 
        except:
          self.push('%s is not exist\r\n' % fileName)
          return 

        sendLine(self, recvName, 'A FILE WILL BE SEND')
        sendLine(self, recvName, 'filename %s' % fileName)

        fd = open(fileName, 'r')
        self.push('----------Send File Begin-----------\r\n')
        while True:
          line = fd.readline()
          if line:
            sendLine(self, recvName, line)
          else:
            break
        sendLine(self, recvName, 'SEND FILE OVER')
        fd.close()
        self.push('-----------Send File Over-----------\r\n')
      else:
        self.push('%s is not in the list\r\n' % self.nickname)

       #---------------------------------------------------
    parts = line.strip().split(' ', 1)
    command = parts[0][1:] #remove the '/'
    try: 
      msg = parts[1]
    except IndexError :
      msg = '' 

    if command == 'exit':
      do_exit(self, msg)
    elif command == 'who':
      self.updateNames()
    elif command == 'file':
      do_file(self, msg)
    elif command in self.server.names:
      do_privateChat(self, command, msg)
    else :
      self.push('Unvalid command : %s\r\n' % command)

  def collect_incoming_data(self, data):
    """
    Collect_incoming_data - receive data
    """
    self.data.append(data)

  def found_terminator(self):
    line = ''.join(self.data)

    if self.isNickname():
      self.getNickname(line)
      self.data = []
    elif self.isCommand(line):
      self.processCommand(line)
      self.data = []
    else :  
      self.data = []
      message = "<%s> %s" % (self.nickname , line)
      self.server.broadcast(self, message+'\r\n')
      print message

  def handle_close(self):
    async_chat.handle_close(self)
    try:
      del self.server.names[self.server.names.index(self.nickname)] 
    except: pass
    self.server.disconnect(self)
    self.updateNames()


class ChatServer(dispatcher): 
  """
  ChatServer - accept the connections and broadcast the message
  to all the clients
  """
  def __init__(self, port):
    dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.set_reuse_addr()
    self.bind(('' , port))
    self.listen(5)

    self.sessions = []
    self.names = []

  def handle_accept(self): 
    sock, addr = self.accept()
    print addr, ' is connected'
    self.sessions.append(ChatSession(self, sock))

  def disconnect(self, session):
    self.sessions.remove(session)

  def broadcast(self, client, line):
    for session in self.sessions:
      session.push(line)

if __name__ == '__main__':
  server = ChatServer(PORT)
  try:
    asyncore.loop()
  except KeyboardInterrupt: 
    pass
