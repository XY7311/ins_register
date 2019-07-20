import random
import re
import time

import pymysql
from selenium import webdriver

from User_Agent import User_Agent
from confir_gmail import confir_gmail
from explicit_wait import explicit_wait
from ins_pymsql import fetch_one_sql, oprt_mysql
from confir_yahoomail import confirm_email, grt_mail_link


class Main():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='root', password='123456',
                                    db='xy_test', charset='utf8')
        
    def ins_reg(self,email,password):
        options = webdriver.ChromeOptions()
        options.add_argument("-lang=en-uk")

        #通过User_Agent随机产生useragent
        # user_agent = random.sample(User_Agent,1)[0]
        # print(user_agent)
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
        options.add_argument('user-agent=' + user_agent)

        port = str(random.sample(range(25501,26000),1)[0])
        print(port)
        options.add_argument("--proxy-server=http://172.16.254.251:"+port)

        chrome_obj = webdriver.Chrome(chrome_options=options)
        chrome_obj.delete_all_cookies()
        chrome_obj.maximize_window()
        chrome_obj.get("https://www.instagram.com")

        fullname = re.findall(".*@",email)[0][:-1]

        ec_params = ['//form[@method="post"]',"XPath"]
        explicit_wait(chrome_obj,"VOEL",ec_params)
        chrome_obj.find_element_by_xpath('//input[@name="emailOrPhone"]').send_keys(email)
        chrome_obj.find_element_by_xpath('//input[@name="fullName"]').send_keys(fullname)
        ec_params = ['//form/div[5]/div/div/div',"XPath"]
        explicit_wait(chrome_obj,"VOEL",ec_params)
        #随机生成用户名
        chrome_obj.find_element_by_xpath('//form/div[5]/div/div/div').click()
        chrome_obj.find_element_by_xpath('//input[@name="password"]').send_keys(password)
        chrome_obj.find_element_by_xpath('//button[@type="submit"]').click()
        
        # 判断是否注册成功
        ec_params = ['//a/div/div/span[@aria-label="Instagram"]']
        explicit_wait(chrome_obj,"VOEL",ec_params)
        if chrome_obj.find_element_by_xpath('//a/div/div/span[@aria-label="Instagram"]'):
            print("registered successfully")
            # User_Agent存数据库
            sql = "update register_account set user_agent=%s where email=%s;"
            oprt_mysql(self.conn,sql,(user_agent,email))
            # 邮箱验证
            try:
                # 点击进入个人主页
                chrome_obj.find_element_by_xpath('//div/div[3]/a/span').click()
                print("Enter the personal page!")
            except:
                pass
            ec_params = ['//section/div/a/button',"XPath"]
            explicit_wait(chrome_obj,"VOEL",ec_params)
            try:
                # 点击编辑主页
                chrome_obj.find_element_by_xpath('//section/div/a/button').click()
            except:
                pass
            ec_params = ['//form/div[7]/div/button',"XPath"]
            explicit_wait(chrome_obj,"VOEL",ec_params)
            try:
                # 点击验证邮箱
                chrome_obj.find_element_by_xpath('//form/div[7]/div/button').click()
            except:
                pass
        else:
            print("registered failed")

        chrome_obj.quit()

    def Run(self):
        sql = "select * from register_account"
        date = fetch_one_sql(self.conn,sql)
        for i in date:
            email = i[1]
            pwd = i[2]
            recovery = i[3]
            self.ins_reg(email,pwd)
            #验证yahoo邮箱
            # confirm_email(grt_mail_link(email,pwd))
            #验证邮箱
            confir_gmail(email,pwd,recovery)


if __name__ == "__main__":
    test = Main()
    test.Run()
