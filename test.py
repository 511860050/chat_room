#!/usr/bin/python
# -*- coding: utf-8 -*-
#============================================
#FileName: test.py
#Date: 2013年 06月 12日 星期三 16:15:52 CST
#Author: chenhuan
#============================================

from Tkinter import *

root = Tk()

frame_1 = Frame(root, width=400, height=400, bg='green')
frame_1.propagate(False)
frame_1.pack(side=LEFT)

text_frame = Frame(frame_1, width=400, height=340, bg='red')
text_frame.propagate(False)
text_frame.pack()

text = Text(text_frame)
text.pack(expand='yes', fill='both', pady=4)

entry = Entry(frame_1)
entry.pack(fill='x', pady=2)

button = Button(frame_1, text='Enter')
button.pack(anchor='se', expand='yes', fill='y')


frame_2 = Frame(root, width=100, height=400,  bg='yellow')
frame_2.propagate(False)
frame_2.pack(side=LEFT, padx=4)

root.mainloop()
