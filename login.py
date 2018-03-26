# encoding=utf-8
from tkinter import *
from tkinter import messagebox
import re
import base64
import json


# 创建 登录界面
class LoginUI:
    def __init__(self):
        self.state = False  # 初始状态为false,即还未登录
        self.r = Tk()
        self.r.title('WordPlayer')
        self.r.geometry('300x125')
        self.name = StringVar()
        self.pswd = StringVar()
        self.l1 = Label(self.r, text='账号')
        self.l1.grid(row=3, column=1)
        self.l2 = Label(self.r, text='密码')
        self.l2.grid(row=4, column=1)
        self.e1 = Entry(self.r, textvariable=self.name)
        self.e1.bind('<Return>', self.ok)  # 回车键确认
        self.e1.grid(row=3, column=2)
        self.e1.focus_set()
        self.e2 = Entry(self.r, textvariable=self.pswd, show='*')
        self.e2.bind('<Return>', self.ok)
        self.e2.grid(row=4, column=2)
        self.v1 = IntVar()
        self.v1.set(1)
        self.rb1 = Radiobutton(self.r, text='登录', variable=self.v1, value=1)
        self.rb1.grid(row=1, column=1, padx=30)
        self.rb2 = Radiobutton(self.r, text='注册', variable=self.v1, value=0)
        self.rb2.grid(row=1, column=2, sticky=E)
        self.bt1 = Button(self.r, text='确认', command=self.reg_or_log)
        self.bt1.grid(row=5, column=1)
        self.bt2 = Button(self.r, text='重输', command=self.re_enter)
        self.bt2.grid(row=5, column=2, sticky=E)
        self.r.mainloop()

    # 选择登录还是注册
    def reg_or_log(self):
        self.get_name = self.name.get().strip()
        self.get_pswd = self.pswd.get().strip()
        if self.get_name == '' or self.get_pswd == '':  # 如果用户未输入信息就提示并重新输入
            messagebox.showwarning(self.r, message='请输入账号或密码！')
            self.re_enter()
            return
        elif not re.match('[a-zA-Z0-9]', self.get_pswd):  # 判断密码格式，不符合标准则提示
            messagebox.showwarning(self.r, message='密码必须是字母和数字的组合！')
            self.re_enter()
            return
        else:
            self.f = open('./Users/usersInfo.json', 'r')
            self.userDict = json.load(self.f)
            self.f.close()
            # 用户选择注册，加密保存用户信息
            if self.v1.get() == 0:
                if self.get_name in self.userDict:
                    messagebox.showerror(message='用户名已存在!')
                    self.re_enter()
                    return
                else:
                    messagebox.showinfo(self.r, message=' 成功注册！')
                    self.userDict[self.get_name] = base64.encodebytes(self.get_pswd.encode()).decode()
                    with open('./Users/usersInfo.json', 'w') as f:
                        json.dump(self.userDict, f)
                    self.state = True
            # 用户选择登录，验证用户信息
            elif self.v1.get() == 1:
                if self.get_name in self.userDict:
                    if self.userDict[self.get_name] == base64.encodebytes(self.get_pswd.encode()).decode():
                        messagebox.showinfo(self.r, message='成功登录！')
                        self.state = True  # 登录状态信号变为true
                    else:
                        messagebox.showerror(self.r, message='密码错误！')
                        self.re_enter()
                        return
                else:
                    messagebox.showerror(self.r, message='用户名错误！')
                    self.re_enter()
                    return

            with open('config', 'w') as f:
                f.write(self.get_name + '\n' + base64.encodebytes(self.get_pswd).decode())
            self.r.destroy()

    def re_enter(self):
        """
        在输入错误的情况下把原先的内容清空以便重新输入
        """
        self.pswd.set('')
        self.name.set('')

    def ok(self, event):
        """回车键事件"""
        self.reg_or_log()


# 如果有配置文件，则自动登录
class Login:
    def __init__(self):
        self.state = False
        self.usr = ''
        self.psw = ''

    def login(self):
        with open('config', 'r') as f:
            account = f.read().split('\n')
            self.usr = account[0]
            self.psw = account[1]
        self.get_name = base64.decodebytes(self.psw.encode()).decode()
        self.state = True
