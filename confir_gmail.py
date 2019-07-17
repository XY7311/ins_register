import email
import imaplib
import poplib
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from selenium import webdriver


def recv_email_by_pop3(email,password):
    pop_server_host = "pop.gmail.com"
    pop_server_port = 995

    #连接服务器
    try:
        email_server = poplib.POP3_SSL(host=pop_server_host, port=pop_server_port, timeout=10)
        print("connect server success")
    except:
        print("email server connect time out")

    # 验证邮箱
    try:
        email_server.user(email)
        print("username existd")
    except:
        print("email address do not exist")
        exit(1)
    # 验证邮箱密码
    try:
        email_server.pass_(password)
        print("password correct")
    except:
        print("password do not correct")
        exit(1)

    # 邮件数量
    email_count = len(email_server.list()[1])
    # 通过retr(index)读取邮件的内容
    resp, lines, octets = email_server.retr(email_count) #最新一封邮件
    email_content = b'\r\n'.join(lines)
    msg=email.message_from_string(email_content.decode())
    email_msg = msg.get_payload(decode=True)
    yjhtml = email_msg.decode('utf8','replace')
    lst = re.findall(r"href=.*>Confirm",yjhtml)
    print("邮件链接为："+lst[0][6:-9])
    # 关闭连接
    email_server.close()
    return lst[0][6:-9]

def confir(email,password):
    href = recv_email_by_pop3(email,password)
    options = webdriver.ChromeOptions()
    options.add_argument("-lang=en-uk")
    chrome_obj = webdriver.Chrome(chrome_options=options)
    chrome_obj.maximize_window()
    chrome_obj.get(href)
    #验证

if __name__ == "__main__":
    email_address = "snlanl18@gmail.com"
    email_password = "iwpB8YySIESm4de"
    confir(email_address,email_password)
