# board-game-manager
one board game manager based on python. learning and coding...\n
this project is for boardgame admissions and searches, folder name and menu in code are in Chinese
save all files in same folder, run boardgame_txtstorgae.py it should work in IDE
这是一个桌游收录以及检索的管理器，文件夹和代码中的提示菜单包含中文名称
保存所有文件到同一文件夹，运行boardgame_txtstorgae.py

这里为更新日志
2022/8/9     基本功能完成（列出全部内容，查询，增加，删除）
             完成class的初始化和文字内容
2022/8/13    完成txt保存输入的部分，现在可用txt保存所有桌游信息，并在开始运行的适合自动读取。
             新增列出桌游时前面会标出序号
2022/8/17    增加英语名称以及英语名称搜索功能。但是还不能模糊查询，大小写敏感还需要改进。（8/30已更新实现）
             修改程序读取txt内容的部分，现在更加简短利于修改。            
             增加修改桌游信息功能。
2022/8/18    完成自动发送保存信息到指定邮箱功能（postman.py），这个功能其实可以独立于这个程序。
             邮箱功能使用smtp发送，已经设置好qq邮箱的服务器和端口，使用time库，可以记录发送所需时间
             还需要在后续加入附件功能（8/30已更新实现） 期望做个规则清单，可以给每个玩家发送附带规则图片的电子邮件
2022/8/26    更新英文查询功能 现在可以忽略大小写查询 .lower()方法
             完善中英文搜索机制 可以模糊查询 输入部分文字就可以搜索完整名字 从 a == b 改成 a in b
2022/8/27    再次更新中英文查询机制 现在可以更模糊地查询 输入内容有部分错字也可以匹配 并增加搜索结果的序号
             使用difflib库 SequenceMatcher() 并用.quick_ratio输出匹配度
             新增按重度排序功能
2022/8/29    完善搜索机制 融合中英文搜索功能 先进行中英文判断再进行对应搜索（使用汉字的正则表达式进行判断）
2022/8/30    重写check_name函数，check_name(name)返回选择列表，如果没有匹配则返回布尔值False
             重写修改桌游信息的部分 完善增加，删除，修改前检查名字的机制，并且增加在这一步可以模糊搜索的功能
             修改邮件发送脚本 更新发送txt文件作为附件的功能
             增加进程内存监测选项，目前没什么用的功能
2022/9/4     新增加一个详细说明功能 选择桌游后打开一个对应的txt文档里面会有开场介绍规则简述和内容清单 文件夹存于子文件夹reception中
2022/9/5     新增一键创建全部桌游名称的txt文件功能 使用os.walk()遍历文件夹 如已创建则不会重新创建 用来完善详细说明功能
             现改为创建对应桌游名称的子文件夹，可在其中加入图片和其他文件描述，期望之后可邮件发送内容
             新增打开对应文件夹功能 使用os.system('open /Users/xx')实现 mac和win不通用
             更新用check_name取缔原有的search模块 减少代码长度
2022/10/3    增加游戏模式描述 已更新库中所有桌游描述
             发现匹配桌游机制有bug 输入玩家人数为1时依然会推荐人数只为2的桌游（10/3 已修复，并减少匹配机制的重复代码）
2022/10/6    修改增加桌游部分由于新增桌游模式造成的bug 新增自动新建文件夹，无需手动添加
