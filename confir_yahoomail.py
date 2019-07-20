import imaplib,email,smtplib,poplib,re
from email.mime.text import MIMEText
from email.header import Header
from selenium import webdriver
# 接收邮件
def grt_mail_link(email_address,email_password):
    pop_server_host = "pop.mail.yahoo.com"
    pop_server_port = 995

    #连接服务器
    try:
        email_server = poplib.POP3_SSL(host=pop_server_host, port=pop_server_port, timeout=10)
        print("connect server success")
    except:
        print("email server connect time out")

    # 验证邮箱
    try:
        email_server.user(email_address)
        print("username existd")
    except:
        print("email address do not exist")
        exit(1)
    # 验证邮箱密码
    try:
        email_server.pass_(email_password)
        print("password correct")
    except:
        print("username do not correct")
        exit(1)

    # 邮件数量
    email_count = len(email_server.list()[1])
    # 通过retr(index)读取邮件的内容
    resp, lines, octets = email_server.retr(email_count) #最新一封邮件
    # resp, lines, octets = email_server.retr(8)
    email_content = b'\r\n'.join(lines)
    msg=email.message_from_string(email_content.decode())
    email_msg = msg.get_payload(decode=True)
    yjhtml = email_msg.decode('utf8','replace')
    lst = re.findall(r'<a href=.*?style',yjhtml)
    email_link = lst[1][9:-6]
    print("email_link："+email_link)
    # 关闭连接
    email_server.close()
    return email_link

def confirm_email(email_link):
    options = webdriver.ChromeOptions()
    options.add_argument("-lang=en-uk")
    chrome_obj = webdriver.Chrome(chrome_options=options)
    chrome_obj.get(email_link)
    chrome_obj.quit()
    
if __name__ == "__main__":
    email_address = "UlyssesDorispQlX@yahoo.com"
    email_password = "k7MST0o59"
    confirm_email(grt_mail_link(email_address,email_password))