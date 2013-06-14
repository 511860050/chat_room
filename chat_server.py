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

class CommandHandler():
  """
  CommandHandler - process the command
  """
  def __init__(self, session, line):
    self.session = session
    self.processCommand(line)
  
  def processCommand(self, line):
    """
    ProcessCommand - process the command
    """
    parts = line.strip().split(' ', 1)
    command = parts[0][1:] #remove the '/'
    try: 
      msg = parts[1]  #message of command
    except IndexError :
      msg = '' 

    if command == 'exit':
      self.do_exit(msg)
    elif command == 'who':
      self.updateNames()
    elif command == 'file':
      self.do_file(msg)
    elif command in self.session.server.names:
      name = command
      self.do_privateChat(name, msg)
    else :
      self.session.push('Unvalid command : %s\n' % command)

  def do_exit(self, msg):
    """
    Do_exit - print the message then exit the chat_server
    command format - /exit
    """
    self.session.server.broadcast('%s is logout %s\n' % \
                                 (self.nickname, msg))

  def sendLine(self, name, msg):
    for session in self.session.server.sessions :
      if name == session.nickname :
        session.push(msg+'\n')

  def do_privateChat(self, name, msg):
    """
    Do_privateChat - private chat 
    command format - /nickname message
    """
    message = "<%s> %s" % (self.session.nickname, msg)
    self.sendLine(name, message)

  def do_file(self, msg):
    """
    Do_file - copy the file from fromAddress to toAddress
    """
    parts = msg.split(' ', 1)
    toAddress = parts[0]
    fileName = parts[1]

    self.session.push('SENDFILE %s %s\n' % (toAddress, fileName))
    self.sendLine(toAddress, 'RECEIVEFILE %s\n' % fileName)

  def updateNames(self):
    """
    Do_who - show the online clients
    command format - /who
    """
    self.session.server.broadcast('UPDATE NAMES\n')
    for name in self.session.server.names:
      self.session.server.broadcast(name+'\n')
    self.session.server.broadcast('UPDATE NAMES OVER\n')

class ChatSession(async_chat) :
  """
  ChatSession - deal with the connection with a client
  """
  def __init__(self, server, sock):
    async_chat.__init__(self, sock)
    self.set_terminator('\n')

    self.data = []
    self.server = server
    self.nickname = ""
    self.nameFlag = False

    self.push("Enter you nickname: \n")
    
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
      self.push('Your nickname is %s\n' % nickname)
    else :
      self.push('Name %s is exist, Enter another one: \n' % nickname) 

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

  def collect_incoming_data(self, data):
    """
    Collect_incoming_data - receive data
    """
    self.data.append(data)
  
  def found_terminator(self):
    line = ''.join(self.data)

    if self.isNickname():  #process nickname
      self.getNickname(line)
      self.data = []
    elif self.isCommand(line):  #process command
      CommandHandler(self, line)      
      self.data = []
    else :  #broadcast message
      self.data = []
      message = "<%s> %s" % (self.nickname , line)
      self.server.broadcast(message+'\n')

  def handle_close(self):
    async_chat.handle_close(self)
    try:
      del self.server.names[self.server.names.index(self.nickname)] 
    except: pass
    self.server.disconnect(self)
    CommandHandler(self, '/who')  #update the names

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

  def broadcast(self, line):
    for session in self.sessions:
      session.push(line)

if __name__ == '__main__':
  server = ChatServer(PORT)
  try:
    asyncore.loop()
  except KeyboardInterrupt: 
    pass
