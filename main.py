import threading
import time
import os
import shutil
import zipfile
import requests
from bs4 import BeautifulSoup

from tkinter import *

url = "http://leagueskin.net/p/download-mod-skin-2020-chn"
html = requests.get(url)
bs = BeautifulSoup(html.text, "lxml")
zipUrl = bs.find(id="link_download3")['href']

installed = 1
lastVersion = None
currentVersion = None
text = None


# 将函数打包进线程
def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护
    t.setDaemon(True)
    # 启动
    t.start()


def domain():
    updateNeeded = updateCheck()
    if updateNeeded:
        install()
    else:
        textInsert("已是最新版本")
    if os.path.exists('name_CN.ini'):
        shutil.copyfile('name_CN.ini', r'C:\Fraps\data\Default\name_CN.ini')
        textInsert("英雄查询文件替换完成")
    os.startfile(r'C:\Fraps\LOLPRO ' + lastVersion + '.exe')
    textInsert("欢乐的时光就要开始了！")

    # 退出
    windowQuit()


# 检查更新
def updateCheck():
    global installed, lastVersion, currentVersion
    # 本地版本
    try:
        for filename in os.listdir(r'C:\Fraps'):
            if ".exe" in filename:
                currentVersion = filename[7:-4].replace('.exe', '')
                textInsert("当前版本：" + currentVersion)
    except FileNotFoundError:
        textInsert("当前未安装LOL Pro")
        installed = 0

    # 最新版本
    lastVersion = bs.find(id="link_download3").text[20:-6]
    textInsert("最新版本：" + lastVersion)
    return currentVersion != lastVersion


# 下载与安装
def install():
    try:
        textInsert("正在下载...")
        r = requests.get(zipUrl)
        with open("lolSkin.zip", "wb") as code:
            code.write(r.content)
            textInsert("下载完成！")

        # 将下载的文件中的Data.lol文件解压，删除下载文件
        textInsert("开始安装...")
        z1 = zipfile.ZipFile('lolSkin.zip', 'r')
        z1.extract('Data.lol')
        z1.close()
        os.remove('lolSkin.zip')

        # 将解压出来的Data.lol解压到安装位置，删除原文件
        z2 = zipfile.ZipFile('Data.lol', 'r')
        # 删除目标文件夹
        if installed:
            shutil.rmtree(r'C:\Fraps')
        z2.extractall('C:')
        z2.close()
        os.remove('Data.lol')
        # 给程序添加版本号
        shutil.move(r'C:\Fraps\LOLPRO.exe', r'C:\Fraps\LOLPRO ' + lastVersion + '.exe')
        textInsert("安装完成！")
    except Exception as e:
        textInsert("============错误============")
        textInsert(e.__str__())

        windowQuit()


# 退出
def windowQuit():
    time.sleep(2)
    window.quit()
    window.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))


# 窗口添加消息
def textInsert(message):
    global text
    text.config(state="normal")
    text.insert(END, message + "\n")
    text.config(state="disabled")
    text.see(END)


class MyFrm(Frame):
    def __init__(self, master):
        self.root = master
        self.screen_width = self.root.winfo_screenwidth()  # 获得屏幕宽度
        self.screen_height = self.root.winfo_screenheight()  # 获得屏幕高度
        # self.root.resizable(False, False)#让高宽都固定
        self.root.update_idletasks()  # 刷新GUI
        self.root.withdraw()  # 暂时不显示窗口来移动位置
        self.root.geometry('%dx%d+%d+%d' % (
            self.root.winfo_width(), self.root.winfo_height(), (self.screen_width - self.root.winfo_width()) / 2,
            (self.screen_height - self.root.winfo_height()) / 2))  # center window on desktop
        self.root.deiconify()


window = Tk()
MyFrm(window)
window.iconbitmap('')
window.overrideredirect(True)
window.geometry('200x100')
window.resizable(width=False, height=False)
window.wm_attributes('-topmost', 1)

text = Text(window)
text.pack()

# 执行主程序
thread_it(domain)

window.mainloop()
