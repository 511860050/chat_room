#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: text.py
#Date: 2013年 06月 10日 星期一 15:13:02 CST
#Author: chenhuan
#============================================

from Tkinter import *

root = Tk()

frame = Frame(root, width=400, height=300)
frame.propagate(False)
frame.pack()

frame_1 = Frame(frame, width=380, height=280)
frame_1.grid_propagate(False)
frame_1.grid(row=0, column=0)

text = Text(frame_1)
text.pack(expand='yes', fill='both')

scrollX = Scrollbar(frame, orient='horizontal')
scrollX.grid(row=1, column=0, sticky='we')

scrollY = Scrollbar(frame, orient='vertical')
scrollY.grid(row=0, column=1, sticky='ns')

root.mainloop()
