#!/usr/bin/env python
# -*- coding: utf-8 -*-

import adnmb

import tkinter as tk


m_list = adnmb.get_menu()


window = tk.Tk()
var = tk.StringVar()

l = tk.Label(window,textvariable=var,bg='yellow',width=4)
l.pack()

lb=tk.Listbox(window)

for item in m_list:
    lb.insert('end', item.get('title'))

def print_selection():
	value=lb.get(lb.curselection())
	var.set(value)
    
btn=tk.Button(window,text='print selection',command=print_selection)
btn.pack()
lb.pack()

window.mainloop()