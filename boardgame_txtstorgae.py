#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 边写边学习，什么都试试
#  2022/8/9     基本功能完成（列出全部内容，查询，增加，删除）
#               完成class的初始化和文字内容
#  2022/8/13    完成txt保存输入的部分，现在可用txt保存所有桌游信息，并在开始运行的适合自动读取。
#               新增列出桌游时前面会标出序号
#  2022/8/17    增加英语名称以及英语名称搜索功能。但是还不能模糊查询，大小写敏感还需要改进。（8/30已更新实现）
#               修改程序读取txt内容的部分，现在更加简短利于修改。
#               增加修改桌游信息功能。
#  2022/8/18    完成自动发送保存信息到指定邮箱功能（postman.py），这个功能其实可以独立于这个程序。
#               邮箱功能使用smtp发送，已经设置好qq邮箱的服务器和端口，使用time库，可以记录发送所需时间
#               还需要在后续加入附件功能（8/30已更新实现） 期望做个规则清单，可以给每个玩家发送附带规则图片的电子邮件
#  2022/8/26    更新英文查询功能 现在可以忽略大小写查询 .lower()方法
#               完善中英文搜索机制 可以模糊查询 输入部分文字就可以搜索完整名字 从 a == b 改成 a in b
#  2022/8/27    再次更新中英文查询机制 现在可以更模糊地查询 输入内容有部分错字也可以匹配 并增加搜索结果的序号
#               使用difflib库 SequenceMatcher() 并用.quick_ratio输出匹配度
#               新增按重度排序功能
#  2022/8/29    完善搜索机制 融合中英文搜索功能 先进行中英文判断再进行对应搜索（使用汉字的正则表达式进行判断）
#  2022/8/30    重写check_name函数，check_name(name)返回选择列表，如果没有匹配则返回布尔值False
#               重写修改桌游信息的部分 完善增加，删除，修改前检查名字的机制，并且增加在这一步可以模糊搜索的功能
#               修改邮件发送脚本 更新发送txt文件作为附件的功能
#               增加进程内存监测选项，目前没什么用的功能
#  2022/9/4     新增加一个详细说明功能 选择桌游后打开一个对应的txt文档里面会有开场介绍规则简述和内容清单 文件夹存于子文件夹reception中
#  2022/9/5     新增一键创建全部桌游名称的txt文件功能 使用os.walk()遍历文件夹 如已创建则不会重新创建 用来完善详细说明功能
#               现改为创建对应桌游名称的子文件夹，可在其中加入图片和其他文件描述，期望之后可邮件发送内容
#               新增打开对应文件夹功能 使用os.system('open /Users/xx')实现 mac和win不通用
#               更新用check_name取缔原有的search模块 减少代码长度
#  2022/10/3    增加游戏模式描述 已更新库中所有桌游描述
#               发现匹配桌游机制有bug 输入玩家人数为1时依然会推荐人数只为2的桌游（10/3 已修复，并减少匹配机制的重复代码）
#  2022/10/6    修改增加桌游部分由于新增桌游模式造成的bug 新增自动新建文件夹，无需手动添加


import difflib  # 检查两个字符串匹配程度
import postman  # 导入邮件自动发送脚本
import psutil  # 外部库需要安装 用来监测进程的内存占用情况
import os  # 检测系统信息和操作系统
import json


# 定义桌游的属性和返回的文本格式
class Boardgame(object):
    def __init__(self, name, en_name, player_number, game_type, game_mode, time, weight, state, intro):
        self.name = name
        self.en_name = en_name
        self.player_number = player_number
        self.game_type = game_type
        self.game_mode = game_mode
        self.weight = weight
        self.time = time
        self.state = state  # 0表示未购买 1表示已购买
        self.intro = intro

    def __str__(self):
        return f'''名字：{self.name}
英文名字：{self.en_name}
游玩人数：{self.player_number}
游戏类型：{self.game_type}
游戏模式：{self.game_mode}
一般游戏时间：{self.time}
重度：{self.weight}
库存状态：{self.state}
游戏简介：{self.intro}'''


# 桌游管理系统的主体部分
class BoardgameManager(object):
    boardgame_list = []

    # 设置开始时默认的桌游
    def start(self):
        file = open('txtstorage.txt', mode='r')
        contents = file.readlines()
        storage_input = []
        # 去除换行符，并把每行内容依次读取进列表
        for msg in contents:
            msg = msg.strip('\n')
            storage_input.append(msg)
        # 按照行数自动分类，如果有新加属性需要改变 n = n+x 的x值
        mid_list = []
        small_list = []
        n = 0
        for msg in storage_input:
            if '名字：' in msg:
                if '英文名字：' not in msg:  # 如果内容里出现名字 则创建一个新的小列表
                    a0 = storage_input[n]
                    b0: list[str] = a0.split('：')
                    small_list = [b0[1]]
            if '名字：' not in msg or '英文名字：' in msg:  # 如果内容里没有出现名字 则往上面创建的小列表里添加内容
                an = storage_input[n]
                bn = an.split('：')
                if len(bn) == 2:
                    small_list.append(bn[1])
            n = n + 1

            if n % 10 == 0:  # 一共有八项内容 所以被九整除后 往中列表里添加小列表
                mid_list.append(small_list)

        BoardgameManager.create_doc(self)
        file.close()
        # print(small_list[1])
        # print(mid_list)
        # print(len(mid_list))

        # 将列表内容添加为类
        for small_list in mid_list:
            a = Boardgame(small_list[0], small_list[1], small_list[2], small_list[3],
                          small_list[4], small_list[5], small_list[6], small_list[7], small_list[8])
            self.boardgame_list.append(a)

    # 列出所有桌游 用了for循环会自动换行
    def show_all_boardgame(self):
        n = 1
        for boardgame in self.boardgame_list:
            print(f'{n}.  {boardgame.name}')
            n = n + 1
        print('')
        print(f'目前库中有{len(self.boardgame_list)}款桌游')

    # 确认名字是否在库中 并返回列表提供选择
    def check_name(self, name):
        counter = 0
        input_words = f'{name}'
        res = True
        name_list = []
        for word in input_words:
            if not '\u4e00' <= word <= '\u9fff':
                res = False
        if res:
            a = False
            for boardgame in self.boardgame_list:
                if name in boardgame.name:
                    a = True
                    name_list.append(boardgame.name)
                ratio = difflib.SequenceMatcher(lambda x: x == " ", name, boardgame.name).quick_ratio()
                if ratio >= 0.5 and not a:
                    a = True
                    name_list.append(boardgame.name)
            if not a:
                return False
        else:
            a = False
            for boardgame in self.boardgame_list:
                if name.lower() in boardgame.en_name.lower():
                    a = True
                    name_list.append(boardgame.name)
                ratio = difflib.SequenceMatcher(lambda x: x == " ", name.lower(),
                                                boardgame.en_name.lower()).quick_ratio()
                if ratio >= 0.6 and not a:
                    a = True
                    name_list.append(boardgame.name)
            if not a:
                return False
        for name in name_list:
            counter += 1
            print(f'{counter}. {name}')
        choice = input('选择桌游序号')
        if choice.isdigit() and int(choice) <= len(name_list):
            choice = int(choice)
        else:
            return False
        name = name_list[choice - 1]
        return name

    # 添加新的内容
    def add_boardgame(self):
        name = input('名字\n')
        a = None
        # 先检查桌游是否已经在库中
        namein = self.check_name(name)
        if namein and input(f'你想输入的是{namein}吗，按y确认，如果不是请输入任意内容或直接回车继续完成添加') != 'y':
            name = namein
        for boardgame in self.boardgame_list:
            if boardgame.name == name:
                a = True
        if a:
            print('游戏已在库中')
        else:
            en_name = input('英文名字\n')
            player_number = input('玩家人数\n')
            game_type = input('游戏类型\n')
            game_mode = input('游戏模式')
            time = input('一般游戏时间\n')
            weight = input('重度\n')
            state = input('库存情况（已有1/没有0）\n')
            intro = input('简介\n')
            self.boardgame_list.append(
                Boardgame(name, en_name, player_number, game_type, game_mode, time, weight, state, intro))
            print(f'{name}添加成功')
        BoardgameManager.create_doc(self)

    # 修改桌游信息
    def edit_boardgame(self, name):
        # 修改菜单的文本
        msg = f'''输入序号选择要修改的内容
        1.名字
        2.英文名字
        3.玩家人数
        4.游戏类型
        5.游戏时间
        6.重度
        7.游戏简介\n'''
        # 先检查桌游是否在库中
        name1 = name
        name = self.check_name(name)
        print(name)
        if name and input(f'你想修改的内容是{name}吗，按y继续') != 'y':
            print(f'{name1} 不在库中')
            return
        else:
            for boardgame in self.boardgame_list:
                if boardgame.name == name:
                    # a = True
                    choose = input(msg)
                    if choose == '1':
                        old_name, new_name = boardgame.name, input('输入新的游戏名\n')
                        boardgame.name = new_name
                        print(f'名字已成功从{old_name}修改为{new_name}\n')
                    elif choose == '2':
                        old_en_name, new_en_name = boardgame.en_name, input('输入新的英文名\n')
                        boardgame.en_name = new_en_name
                        print(f'名字已成功从{old_en_name} 修改为{new_en_name}\n')
                    elif choose == '3':
                        old_player_number, new_player_number = boardgame.player_number, input('输入新的玩家人数\n')
                        boardgame.player_number = new_player_number
                        print(f'玩家人数已成功从{old_player_number}修改为{new_player_number}\n')
                    elif choose == '4':
                        old_game_type, new_game_type = boardgame.old_game_type, input('输入新的游戏类型\n')
                        boardgame.game_type = new_game_type
                        print(f'游戏类型已成功从{old_game_type}修改为{new_game_type}\n')
                    elif choose == '5':
                        old_time, new_time = boardgame.time, input('输入新的游戏时间\n')
                        boardgame.time = new_time
                        print(f'重度已成功从{old_time}修改为{new_time}\n')
                    elif choose == '6':
                        old_weight, new_weight = boardgame.weight, input('输入新的重度\n')
                        boardgame.weight = new_weight
                        print(f'重度已成功从{old_weight}修改为{new_weight}\n')
                    elif choose == '7':
                        new_intro = input('输入新的桌游简介\n')
                        boardgame.intro = new_intro
                        print(f'桌游简介已成功修改为{new_intro}\n')
                    else:
                        print('数字输错了嗷')
                        return

    # 删除对应名字的桌游
    def delete_boardgame(self, name):
        a = None
        # 先检查桌游是否在库中
        name = self.check_name(name)
        if name and input(f'你想删除的内容是{name}吗，按y继续') != 'y':
            return
        # 遍历库查找匹配名字
        for boardgame in self.boardgame_list:
            if boardgame.name != name:
                continue
            else:
                if input(f'请再次确认是否删除{name}，确认请输入y\n') == 'y':
                    self.boardgame_list.remove(boardgame)
                    print(f'{name}删除成功')
                    a = True
                else:
                    return
        if not a:
            print('找不到该桌游，无法删除')

    # 用条件筛选所有桌游并给出匹配项
    def match_boardgame(self, game_type, player_number, difficulty):
        game_list = list()
        a = b = None
        i = 1
        int(player_number)
        for Boardgame1 in self.boardgame_list:
            if Boardgame1.game_type == f'{game_type}' or game_type == '都行':
                if len(Boardgame1.player_number) != 1 and Boardgame1.state != '0':
                    a, b = Boardgame1.player_number.split('-')
                    int(a)
                    int(b)
                    if a <= player_number <= b:
                        boardgame_weight = float(Boardgame1.weight)
                        if difficulty == '简单':
                            if boardgame_weight <= 2.0:
                                game_list.append(Boardgame1)
                        elif difficulty == '中等':
                            if boardgame_weight <= 3.5:
                                game_list.append(Boardgame1)
                        elif difficulty == '困难':
                            if boardgame_weight <= 5.0:
                                game_list.append(Boardgame1)
        if len(game_list) == 0:
            print('系统没有找到匹配的桌游')
        else:
            print('\n系统给您推荐的桌游为')
            for Boardgame1 in game_list:
                print(f'{i}.  {Boardgame1.name}')
                i = i + 1

    # 按照重度将所有桌游排列
    def sorted_by_weight(self):
        sorted_list = sorted(self.boardgame_list, key=lambda x: x.weight)
        n = 1
        print('重度从低到高排序')
        for boardgame in sorted_list:
            print(f'{n}.  {boardgame.name}  ->{boardgame.weight}')
            n += 1

    # 打开对应名字的txt文件并打印内容
    def txt_boardgame(self, name):
        file_name = self.check_name(name)
        txt_file = open(f'reception/{file_name}/{file_name}.txt', mode='r')
        print(txt_file.read())

    # 遍历文件夹和桌游列表，如果有新增则创建对应名字的文件夹
    def create_doc(self):
        for boardgame in self.boardgame_list:
            path = f'reception/{boardgame.name}/'
            if not os.path.exists(path):
                os.makedirs(path)
                file_open = open(f'{path}{boardgame.name}.txt', mode='w')
                file_open.close()
                # print(path + '创建成功')

    def search_and_open(self, name):
        name = self.check_name(name)
        os.system(f'open /Users/shuojiayan/Desktop/BoardgameManager/reception/{name}')
        print(f'{name}文件夹已打开')
        return

    # 用户交互菜单
    def menu(self):  # 用户菜单
        self.start()
        menu_txt = '''
        •--- •--- • •--- •--- • •--- •--- •
        桌游
        1.列出所有桌游
        2.查询桌游名字
        3.增加桌游
        4.删除桌游
        5.系统匹配桌游
        6.修改桌游信息
        7.按照重度排序
        8.打开对应文件夹
        9.发送数据库到邮箱
        0.退出系统
        •--- •--- • •--- •--- • •--- •--- •
        '''
        n = 0
        while True:
            n = n + 1
            if n != 1 and input('\n 回车后继续 •--- •--- • •--- •--- • •--- •--- • ') != '':
                continue  # 这一段是为了取消第一次输入前出现回车后继续的内容
            print(menu_txt)
            choice = input('请选择需要进行的操作，输入序号\n')
            print('')
            if choice == '1':
                self.show_all_boardgame()
                continue
            elif choice == '2':
                name = input('想要查询的桌游名字是\n')
                name = self.check_name(name)
                for boardgame in self.boardgame_list:
                    if name == boardgame.name:
                        print(boardgame)
                if not name:
                    print('找不到该游戏')
                continue
            elif choice == '3':
                self.add_boardgame()
                self.create_doc()
                continue
            elif choice == '4':
                name = input('想要删除的桌游名字是\n')
                self.delete_boardgame(name)
                continue
            elif choice == '5':
                game_type = input("想要游玩的游戏类型（毛线/德式/美式/都行）\n")
                player_number = input('玩家人数\n')
                difficulty = input('可以接受的最大游戏难度（简单/中等/困难）\n')
                self.match_boardgame(game_type, player_number, difficulty)
                continue
            elif choice == '6':
                name = input('想要修改的游戏名是\n')
                self.edit_boardgame(name)
                continue
            elif choice == '7':
                self.sorted_by_weight()
                continue
            elif choice == '8':
                name = input('想要搜索的桌游名字是\n')
                self.search_and_open(name)
                continue
            elif choice == '9':
                postman.mail()
                continue
            elif choice == '0':
                print('拜拜～')
                break
            elif choice == '01':
                # 隐藏的功能选项
                ram()
                continue
            else:
                print('输对一下数字，秋梨膏')
                continue


# 监测进程的内存占用
def ram():
    print(u'当前进程的内存使用：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))


# 运行部分
boardgameManager = BoardgameManager()
boardgameManager.menu()

# 写入txt保存运行结果
file_handle = open('txtstorage.txt', mode='w')
for Boardgame in boardgameManager.boardgame_list:
    file_handle.write(f'{Boardgame}')
    file_handle.write(' ')
    file_handle.write('\n')
    file_handle.write('\n')
file_handle.close()

# 写入json保存运行结果
with open('jsonstorage.json', mode='w', encoding='utf-8') as f:
    data = []
    for Boardgame in boardgameManager.boardgame_list:
        data.append(Boardgame)
    json.dump(data, f, ensure_ascii=False, indent=4)
