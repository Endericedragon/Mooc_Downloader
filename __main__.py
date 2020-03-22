import network
import parseList
import createFolder
import process

import os
import tkinter
from tkinter import messagebox
# ~ import re
# ~ import pickle
'''
全程使用session
首先获取tid —— 搞定
记得https转成http —— 搞定
同时还要搞到courseList页面获得文件夹关系，文件名以及contentId，Id —— 搞定
根据contentId和id获取'NTESSTUDYSI'(Key)最后搞到signature，下载地址就有了 —— 搞定
调用creater建立文件夹，aria2c下载文件
'''
def main():
    courseUrl = network.https2http(input('请输入课程网址:'))
    courseName = network.getCourseName(courseUrl)
    courseTid = network.getTid(courseUrl)
    courseList = network.getList(courseTid)
    courseDict = parseList.parser(courseList, courseUrl)
    createFolder.creater(courseName, courseDict)
    process.m3u8Process(courseName, courseDict)
    tk = tkinter.Tk()
    tk.withdraw()
    messagebox.showinfo(title = '提示', message = '下载已全部完成!')
if (__name__=='__main__'):
    main()
