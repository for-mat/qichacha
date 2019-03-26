# -*- coding: utf-8 -*-

from Tkinter import *
import pymysql

db = pymysql.connect(host='192.168.1.100', port=3306, user='qcc', passwd='VhO4fNROWARt', db='spider_qichacha',charset='utf8')
cursor = db.cursor()



top = Tk()

top.title("查询")    # 设置窗口标题
top.geometry('250x100')    # 设置窗口大小

Label(top,text="请输入id：").grid(row = 0,column =0,sticky=W)
name = Entry()
name.grid(row = 0,column =1,sticky=W)

def printhello():
    id = name.get()
    cursor.execute('select * from company where id=  %s'%id)
    result = cursor.fetchone()

    a = Tk()
    a.title('ddd')
    a.geometry('670x330')
    t = Text(a,width=95,height=25)
    t.grid(padx=0,pady=0,sticky=W)
    t.insert(END,result)


Button(top, text="查找", command=printhello).grid(row = 1,column =1)

# 进入消息循环
top.mainloop()












