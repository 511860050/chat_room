#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: test.py
#Date: 2013年 06月 12日 星期三 16:15:52 CST
#Author: chenhuan
#============================================

import re

def fuck(line):
  endPattern = re.compile(r'SENDFILEOVER\n$')
  if not endPattern.search(line):
    print 'recvFile: ', line
  else: 
    if line == 'SENDFILEOVER\n': 
      pass
    else:
      otherPart = re.compile(r'(.+)SENDFILEOVER\n$')
      line = otherPart.match(line).group(1)
      print 'recvFile: ', line
