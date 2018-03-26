# encoding=utf-8
import os
import login
from app import MyApp

if __name__ == '__main__':
    if os.path.isfile('config'):
        wel_page = login.Login()
        wel_page.login()
    else:
        wel_page = login.LoginUI()

    # 没有注册登录则避免显示软件主界面
    try:
        if wel_page.state == True:
            main_page = MyApp(wel_page)
    except AttributeError:
        pass
