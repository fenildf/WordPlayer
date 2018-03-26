# encoding=utf-8
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import urllib.request
import time
import random
import re
import os
import pickle


# TODO 可以用 destroy-重建的方法解决前一题对后一题布局干扰的问题
# 创建 主程序界面
class MyApp:
    def __init__(self, state):
        self.root = Tk()
        self.root.minsize(820, 500)
        self.root.title('玩转单词')
        self.ft = font.Font(font=('Microsoft YaHei', 12, 'normal'))
        self.userName = state.get_name
        # 以下菜单部分分为  出题词库、题目形式、附加功能、其他信息
        self.m = Menu(self.root)
        self.root.config(menu=self.m)
        self.m1 = Menu(self.m)  ##### 菜单一
        self.m.add_cascade(label="词库", menu=self.m1)
        self.m1.add_radiobutton(label="四级", command=self.getCET4)
        self.m1.add_radiobutton(label="六级", command=self.getCET6)
        self.m1.add_radiobutton(label="其它", command=self.getOthers)
        self.m2 = Menu(self.m)  ##### 菜单二
        self.m.add_cascade(label="形式", menu=self.m2)
        self.m2.add_radiobutton(label="填空题", command=self.wordCompletion)
        self.m21 = Menu(self.m2)
        self.m2.add_cascade(label='选择题', menu=self.m21)
        self.m21.add_radiobutton(label='英-->汉', command=self.en_to_ch)
        self.m21.add_radiobutton(label='汉-->英', command=self.ch_to_en)
        self.m3 = Menu(self.m)  ##### 菜单三
        self.m.add_cascade(label='功能', menu=self.m3)
        self.m3.add_command(label='增词', command=self.addWord)
        self.m3.add_command(label='查词', command=self.searchWord)
        self.m3.add_command(label='批量查单词', command=self.processWords)
        self.m31 = Menu(self.m3)
        self.m3.add_cascade(label='分析', menu=self.m31)
        self.m31.add_command(label='四级词汇', command=self.analyseCET4)
        self.m31.add_command(label='六级词汇', command=self.analyseCET6)
        self.m4 = Menu(self.m)  ##### 菜单四
        self.m.add_cascade(label="关于", menu=self.m4)
        self.m4.add_command(label='信息', command=self.about)
        self.m4.add_command(label='用户', command=self.usersInfo)
        # 下面的frame用来输出用户答题的判断结果
        self.f2_0 = Frame(self.root, height=125, width=600, bd=4, bg='DarkGray')
        self.f2_0.place(x=0, y=380)
        # 下面的构件主要是 错词展示栏(misWords)和当前时间栏(l2)
        self.count_of_mis = 0  # 错题数量
        self.count_of_qs = 0  # 总题目数
        self.f3 = Frame(self.root, height=500, width=200, bd=4, bg='DimGray')
        self.f3.place(x=600, y=0)
        self.l1 = Label(self.f3, text='   <错词展示栏>    0/0', font=self.ft, fg='yellow', bg='DimGray')
        self.l1.place(x=0, y=0)
        self.misWords = Listbox(self.f3, height=480, width=300, fg='red', bg='SkyBlue')
        for i in range(700):
            self.misWords.insert(1, ' ')
        self.sl = Scrollbar(self.root)
        self.sl.pack(side=RIGHT, fill=Y)
        self.misWords['yscrollcommand'] = self.sl.set
        self.sl['command'] = self.misWords.yview
        self.misWords.place(x=0, y=30)
        # 时间栏
        self.l2 = Label(self.f3, text="", height=2, width=28, bg='#383838', fg='white')
        self.l2.place(x=0, y=460)
        self.update_clock()

        self.root.mainloop()

    def update_clock(self):
        """
        更新时间
        """
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.l2.configure(text=now)
        self.root.after(1000, self.update_clock)

    # 下面4个函数获取词库单词
    def getFiles(self, name):
        """
        打开词库文件，读取所有行(每行只有一个单词及其翻译)
        """
        if name == '':  # 给出文件对话框供用户选择词库
            self.filename = filedialog.askopenfilename(filetypes=[("all files", "*")], initialdir='./Lexicon')
            try:
                self.f1 = open(self.filename, 'r', encoding='utf8')
                self.lines = self.f1.readlines()
                self.f1.close()
            except:
                messagebox.showerror('Error', '不能打开文件\n' + str(sys.exc_info()[1]))
            if self.filename == ():
                messagebox.showwarning('Warning', "请选择文件!")
                return
            else:
                messagebox.showinfo('Info', '成功打开文件%s' % str(self.filename.encode('utf8')))
        else:
            self.filename = './Lexicon/' + name
            self.f1 = open(self.filename, 'r')
            self.lines = self.f1.readlines()
            self.f1.close()

    def getWords(self):
        """
        从之前的列表中选单词作为出题单词
        """
        self.aLine, self.word, self.expre, self.word1, self.word2, self.word3, self.expre1, self.expre2, self.expre3 \
            = '', '', '', '', '', '', '', '', ''
        while '' in [self.aLine, self.word, self.expre, self.word1, self.word2,
                     self.word3, self.expre1, self.expre2, self.expre3]:  # 防止词库文件有有空行
            try:
                self.aLine = self.lines[random.randint(1, len(self.lines))]
                self.word = self.aLine.split()[0].strip()
                self.expre = self.aLine.split()[1].strip()
                self.word1 = self.lines[random.randint(1, len(self.lines))].split()[0].strip()
                self.word2 = self.lines[random.randint(1, len(self.lines))].split()[0].strip()
                self.word3 = self.lines[random.randint(1, len(self.lines))].split()[0].strip()
                self.expre1 = self.lines[random.randint(1, len(self.lines))].split()[1].strip()
                self.expre2 = self.lines[random.randint(1, len(self.lines))].split()[1].strip()
                self.expre3 = self.lines[random.randint(1, len(self.lines))].split()[1].strip()
            except:
                return None  # none信号 可表明用户没有选词库
        return True

    def getCET4(self):
        """
        指定读取四级词汇
        """
        self.getFiles('CET_4.txt')

    def getCET6(self):
        """
        指定读取六级词汇
        """
        self.getFiles('CET_6.txt')

    def getOthers(self):
        """
        由用户自己选择词库
        """
        self.getFiles('')

    # 填空题
    def wordCompletion(self):
        if self.getWords() is None:  # 防止用户未选词库就点击题型
            messagebox.showerror(message='请先选择词库！')
            return
        messagebox.showwarning(title='Tips', message='输完按 回车键 即可判断并切换')

        # 出题
        def ques():
            global v2
            self.getWords()
            f1 = Frame(self.f1_1, bd=4, relief="groove", height=100, width=100)
            f1.place(x=165, y=100)
            Label(f1, text=self.expre, height=3, width=25, font=self.ft).grid()
            v2 = StringVar()
            e = Entry(f1, width=20, bd=2, textvariable=v2)
            e.bind('<Return>', next_one)
            e.grid()
            Label(f1, text=' ').grid()

        # 判断
        def judge():
            f2_1 = Frame(self.root, height=125, width=600, bd=4, bg='DarkGray')
            f2_1.place(x=0, y=380)

            f2 = Frame(f2_1, relief="groove", height=100, width=100)
            f2.place(x=180, y=0)
            if v2.get() == '' or v2.get().strip().lower() != self.word:  # 答错则保存到错词本
                with open('./Users/' + self.userName + '_misWords.txt', 'a+') as f:
                    item = self.word + '   ' + self.expre + '\n'
                    f.write(item)
                wrong_ans = Label(f2, text='回答错误!\n正确答案是 %s\n已为您添加至错词本！' % self.word, width=25, font=self.ft)
                wrong_ans.grid()
                self.misWords.insert(0, item)  # 答错的词显示在"错词展示栏"界面
                self.count_of_mis += 1
            else:
                right_ans = Label(f2, text='回答正确！', width=25, font=1)
                right_ans.grid()
            self.count_of_qs += 1
            ques()
            self.l3 = Label(self.f3, text='   <错词展示栏>    %s/%s' % (str(self.count_of_mis), str(self.count_of_qs)),
                            font=self.ft, fg='yellow', bg='DimGray')  # 更新  "错词展示栏"
            self.l3.place(x=0, y=0)

        def next_one(event):
            """
            判断这一题，显示下一题
            """
            judge()

        self.f1_1 = Frame(self.root, height=380, width=600, bd=4, bg='PaleGreen')
        self.f1_1.place(x=0, y=0)
        ques()
        self.bt1 = Button(self.f1_1, text='确认', bd=2, width=8, command=judge)
        self.bt1.place(x=265, y=240)

    # 选择题
    def wordChoice(self):
        if self.getWords() is None:  # 防止用户未选词库就点击题型
            messagebox.showerror(message='请先选择词库！')
            return
        messagebox.showwarning(title='Tips', message='对着选项双击左键即可判断并切换')

        # 出题
        def ques():
            global v3, center, rightItem, rightAns
            self.getWords()
            if self.model == 1:  # 英--->汉
                center, rightAns, ops2, ops3, ops4 = self.word, self.expre, self.expre1, self.expre2, self.expre3
            else:  # 汉--->英
                center, rightAns, ops2, ops3, ops4 = self.expre, self.word, self.word1, self.word2, self.word3
            v3 = IntVar()
            ops = [rightAns, ops2, ops3, ops4]
            random.shuffle(ops)  # 打乱顺序
            A, B, C, D = ops
            rightItem = ops.index(rightAns)

            f3 = Frame(self.f1_2, bd=4, relief="groove", height=100, width=100)
            f3.place(x=180, y=80)
            Label(f3, text=center, width=20, font=self.ft, bd=2).grid()
            rb1 = Radiobutton(f3, text=A, variable=v3, value=0, height=1, font=self.ft)
            rb2 = Radiobutton(f3, text=B, variable=v3, value=1, height=1, font=self.ft)
            rb3 = Radiobutton(f3, text=C, variable=v3, value=2, height=1, font=self.ft)
            rb4 = Radiobutton(f3, text=D, variable=v3, value=3, height=1, font=self.ft)
            rb1.bind('<Double-Button-1>', next_one)
            rb2.bind('<Double-Button-1>', next_one)
            rb3.bind('<Double-Button-1>', next_one)
            rb4.bind('<Double-Button-1>', next_one)
            rb1.grid(stick=W)
            rb2.grid(stick=W)
            rb3.grid(stick=W)
            rb4.grid(stick=W)

        # 判断
        def judge():
            f2_2 = Frame(self.root, height=125, width=600, bd=4, bg='DarkGray')
            f2_2.place(x=0, y=380)
            f4 = Frame(f2_2, relief="groove", height=100, width=100)
            f4.place(x=180, y=0)
            if v3.get() == rightItem:
                right_ans = Label(f4, text='回答正确！', width=25, font=self.ft)
                right_ans.grid()
            else:  # 答错则保存到错词本 "
                with open('./Users/' + self.userName + '_misWords.txt', 'a+') as f:
                    if self.model == 1:
                        item = center + '   ' + rightAns + '\n'
                    else:
                        item = rightAns + '   ' + center + '\n'
                    f.write(item)
                wrong_ans = Label(f4, text='回答错误!\n正确答案是  %s\n已为您添加至错词本！' % rightAns, width=30, font=self.ft)
                wrong_ans.grid()
                self.misWords.insert(0, item)
                self.count_of_mis += 1
            ques()
            self.count_of_qs += 1
            self.l4 = Label(self.f3, text='   <错词展示栏>    %s/%s' % (str(self.count_of_mis), str(self.count_of_qs)),
                            font=self.ft, fg='yellow', bg='DimGray')  # 更新 "错词展示栏"
            self.l4.place(x=0, y=0)

        def next_one(event):
            """
            判断这一题，显示下一题
            """
            judge()

        self.f1_2 = Frame(self.root, height=380, width=600, bd=4, bg='PaleGreen')
        self.f1_2.place(x=0, y=0)
        ques()
        self.bt2 = Button(self.f1_2, text='确认', bd=2, width=8, command=judge)
        self.bt2.place(x=260, y=280)

    def en_to_ch(self):
        """
        英--->汉
        """
        self.model = 1
        self.wordChoice()

    def ch_to_en(self):
        """
        汉--->英
        """
        self.model = 0
        self.wordChoice()

    # 下面三个函数主要是查词、给个人词库中增词
    def haici(self, word):
        """
        用"海词"网站查单词
        """
        self.url = 'http://dict.cn/'
        self.url += word
        try:
            self.page = urllib.request.urlopen(self.url)  # 获取网页源代码
            pattern1 = re.compile('<ul class="dict-basic-ul">([\s\S]*?)</ul>')
            pattern2 = re.compile('<span>(.*)</span>')
            pattern3 = re.compile('<strong>(.*)</strong>')
            self.data = self.page.read().decode('utf8')
            trans_content = re.findall(pattern1, self.data)
            trans1 = re.findall(pattern2, trans_content[0])
            trans2 = re.findall(pattern3, trans_content[0])
            trans_all = ''
            for i in range(min(len(trans1), len(trans2))):
                trans_all += trans1[i] + trans2[i] + '\n'
            if trans_content:
                return trans_all
            else:
                return 'None'
        except:
            return 'None'

    def search(self, word):
        dictfile = open('Lexicon/localDict.pkl', 'rb')
        localDict = pickle.load(dictfile)
        dictfile.close()
        if word in localDict:
            return localDict[word]
        else:
            return self.haici(word)

    def addWord(self):
        def add_it():
            word = self.v4.get().lower()
            if word == '':
                return
            trans = self.search(word)
            with open('./Users/' + self.userName + '_addWords.txt', 'a+', ) as f:
                if trans != None:
                    item = word + '   ' + trans + '\n'
                    f.write(item.encode('gbk'))  # 论编码的重要性，，，
                    Label(self.top1, text='成功加入！').grid(row=2)
                else:
                    Label(self.top1, text='查无此词！').grid(row=2)
            self.v4.set('')

        def ok(event):
            add_it()

        self.top1 = Toplevel()
        self.top1.wm_attributes('-topmost', 1)  # 使查词的子窗口始终置于最前面
        self.v4 = StringVar()
        self.e11 = Entry(self.top1, textvariable=self.v4, bd=2)
        self.e11.bind('<Return>', ok)
        self.e11.grid(padx=4, pady=4)
        self.e11.focus_set()
        self.bt3 = Button(self.top1, text='确认', command=add_it)
        self.bt3.grid()
        Label(self.top1, text='').grid(row=2)

    def searchWord(self):
        def search_it():
            word = self.v5.get().lower()
            trans = self.search(word)
            if trans != 'None':
                messagebox.showinfo(title='查询结果', message=trans)
            else:
                messagebox.showinfo(title='查询结果', message='None！')
            self.v5.set('')

        def ok(event):
            search_it()

        self.top2 = Toplevel()
        self.top2.wm_attributes('-topmost', 1)  # 子窗口置于最前面
        self.v5 = StringVar()
        self.e22 = Entry(self.top2, textvariable=self.v5, bd=2)
        self.e22.bind('<Return>', ok)
        self.e22.grid(padx=4, pady=4)
        self.e22.focus_set()
        self.bt4 = Button(self.top2, text='确认', command=search_it)
        self.bt4.grid()

    def processWords(self):
        """
        批量查单词，待查单词应该是每行一个单词的文本文件。
        """
        filePath = filedialog.askopenfilename(
            filetypes=[("all files", "*")], initialdir='./Raw_words/')
        try:
            file = open(filePath, 'r')
            wordlist = sorted(list(set(file.readlines())))
            file.close()
        except:
            messagebox.showerror('Error', '无法打开文件\n%s' % str(sys.exc_info()[1]))
            return
        if filePath == ():
            messagebox.showwarning('Warning', "请选择文件!")
            return
        else:
            messagebox.showinfo('Info', '正在处理中，请确认并等待')

        count_of_words = len(wordlist)
        dictfile = open('./Lexicon/localDict.pkl', 'rb')
        localDict = pickle.load(dictfile)
        dictfile.close()
        fileName = os.path.basename(filePath)

        start = time.time()
        failedList = []
        with open('./Lexicon/%s' % fileName, 'w') as f:
            for word in wordlist:
                word = word.strip()
                if word in localDict:
                    trans = localDict[word]
                else:
                    trans = self.haici(word).replace('\n', ' ').strip()
                if trans != 'None':
                    f.write(word + '    ' + trans + '\n')
                else:
                    failedList.append(word)
        with open('./Lexicon/%s' % ('failedWords-' + fileName), 'w') as f:
            for failedWords in failedList:
                f.write(failedWords + '    None\n')
        end = time.time()
        interval = end - start

        messagebox.showinfo(message='用时%s秒\n处理单词共%s条\n请在 Lexicon 文件夹中查看' % ('%.2f' % interval, count_of_words))

    def analyseText(self, referenceText, name):
        """
        从英文文章中分析出四六级单词
        """
        filename = filedialog.askopenfilename(
            filetypes=[("all files", "*")], initialdir='./Texts')
        try:
            self.f2 = open(filename, 'r')
            self.data = self.f2.read()
            self.data = self.data.lower()
            for ch in ",.;~!@#$%^&*()_+=-:":
                self.data = self.data.replace(ch, ' ')
            self.data = self.data.split()
            self.f2.close()
        except:
            messagebox.showerror('Error', '无法打开文件\n%s' % str(sys.exc_info()[1]))
        if filename == ():
            messagebox.showwarning('Warning', "请选择文件!")
            return
        else:
            messagebox.showinfo('Info', '正在分析中，请稍等。。。')

        self.count_of_words = 0
        start = time.time()
        self.word_of_text = open(
            './Texts/%s' % os.path.basename(filename), 'a+')  # 用来存放分析出的单词
        for line in open('./Lexicon/' + referenceText):
            try:
                self.word = line.strip().split()[0]
                self.trans = line.strip().split()[1]
                if self.word in self.data:
                    self.item = self.word + '   ' + self.trans + '\n'
                    self.word_of_text.write(self.item)
                    self.count_of_words += 1
            except:
                pass
        end = time.time()
        interval = end - start
        self.word_of_text.close()
        messagebox.showinfo(message='用时%s秒\n析出单词共%s条\n请在 Texts 文件夹中查看' % ('%.2f' % interval, self.count_of_words))

    def analyseCET4(self):
        """
        从文本中找四级单词
        """
        self.analyseText('CET_4.txt', 'cet4')

    def analyseCET6(self):
        """
        从文本中找六级单词
        """
        self.analyseText('CET_6.txt', 'cet6')

    def about(self):
        """
        软件信息
        """

        def ok(event):
            self.top3.destroy()

        self.top3 = Toplevel()
        self.lb1 = Listbox(self.top3, fg='white', bg='black', height=4, width=30)
        self.lb1.insert(1, 'Author: Duan Yunzhi')
        self.lb1.insert(2, 'Made on: 2017/6/1')
        self.lb1.insert(3, 'Contact: d15821917291@gmail.com')
        self.lb1.insert(4, 'Personal Page: clouduan.github.io')
        self.lb1.bind('<Return>', ok)
        self.lb1.grid(padx=3, pady=4)
        self.top3.mainloop()

    def usersInfo(self):
        """
        用户信息
        """

        def ok(event):
            self.top4.destroy()

        self.top4 = Toplevel()
        self.lb2 = Listbox(self.top4, fg='white', bg='black', height=3)
        self.lb2.insert(1, 'Current User:')
        self.lb2.insert(1, self.userName)
        self.lb2.bind('<Return>', ok)
        self.lb2.grid(padx=3, pady=4)
        self.top4.mainloop()
