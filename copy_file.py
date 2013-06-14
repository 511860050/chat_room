#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: copy_file.py
#Date: 2013年 06月 13日 星期四 14:43:15 CST
#Author: chenhuan
#Usage: copy the file
#============================================

import os
import sys

if len(sys.argv) != 3:
  print 'Usage: %s [from] [to]' % sys.argv[0]
  exit(-1)

try:
  fromFile = open(sys.argv[1].strip(), 'r')
except:
  print 'Error in open r'
  exit(-1)

try:
  toFile = open(sys.argv[2].strip(), 'w')
except:
  print 'Error in open w'
  exit(-1)

while True:
  line = fromFile.readline().strip()
  if line != '':
    toFile.write(line)
  else: break
