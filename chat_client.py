#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: chat_client.py
#Date: 2013年 06月 08日 星期六 16:16:14 CST
#Author: chenhuan
#Usage: chat client
#============================================

import socket
import sys
import os
from threading import Thread

class StandardInput(Thread):
  """
  StandardInput - get the inputs from standard input 
  and send them to the sock
  """
  def __init__(self, writeFd):
    Thread.__init__(self)
    self.setDaemon(True)
    self.writeFd = writeFd
    self.done = False

  def run(self):
    while not self.done:
      #the I/O buffer need to be considerred
      inputText = sys.stdin.readline().strip()
      if inputText:
        self.writeFd.write(inputText+'\r\n')

class ChatClient:
  """
  Chat_Client - build the connection to Chat_Server
  """
  def __init__(self, serverAddr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serverAddr, port))

    try :
      self.readFd = sock.makefile('rb', 0)
      self.writeFd = sock.makefile('wb', 0)
    except :
      print 'Error in sock.makefile'

    self.run()

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

  def run(self):
    """
    Run - get the inputs from standard input and send them to the socket
    and get the inputs from socket and send them to the stdout
    """
    #process the communication between socket and standard input
    standardInput = StandardInput(self.writeFd)
    standardInput.start()
    #process the communication between socket and standard output
    inputText = True
    while inputText:
      inputText = self.readFd.readline()
      if inputText == 'A FILE WILL BE SEND\r\n':
        print 'A file will be send'
        print '---------Receive File Begin-------------'
        self.receiveFile()
        print '----------Receive File Over-------------'
      else:
        print inputText.strip()

    standardInput.done = True    

#-------------------------------------------------------------
if __name__ == '__main__':
  if len(sys.argv) != 3 :
    print 'Usage %s [address] [port]' % sys.argv[0]
    exit(-1)

  ChatClient(sys.argv[1], int(sys.argv[2]))
