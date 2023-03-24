import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# 自动发送邮件的功能
def mail():
    # 记录程序开始时间
    t1 = time.time()

    my_sender = 'shuojiayan@qq.com'  # 发件人邮箱账号
    my_pass = 'bsjszkqibuihbbia'  # 发件人邮箱授权码
    my_user = input('请输入邮箱地址\n')  # 收件人邮箱账号
    ret = True

    try:
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header("From Louie's Python script", 'utf-8')  # 发件人信息
        message['To'] = Header("Louie", 'utf-8')  # 收件人信息
        subject = '桌游信息库'  # 主题
        message['Subject'] = Header(subject, 'utf-8')

        file = open('txtstorage.txt', mode='r')
        message.attach(MIMEText(file.read(), 'plain', 'utf-8'))
        # message.attach(MIMEText('详细内容请看附件', 'plain', 'utf-8'))

        # 传送当前目录下的 txt 文件
        att1 = MIMEText(open('txtstorage.txt', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="txtstorage.txt"'
        message.attach(att1)

        print('正在尝试登陆邮件服务器•--- •--- •')
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # SMTP服务器 端口25
        server.login(my_sender, my_pass)
        print('正在尝试发送邮件•--- •--- •')
        server.sendmail(my_sender, [my_user, ], message.as_string())
        server.quit()

    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False

    #     记录发送完成时的时间
    t2 = time.time()

    # 返回结果
    if ret:
        print('发送成功')
    else:
        print('发送失败')
    #     计算发送所需时间
    t = t2 - t1
    print(f'本次发送耗时{(round(t, 3))}秒')


# mail()
