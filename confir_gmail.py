import time
from selenium import webdriver
from explicit_wait import explicit_wait

def confir_gmail(email,pwd,recovery):
    options = webdriver.ChromeOptions()
    options.add_argument("-lang=en-uk")
    chrome_obj = webdriver.Chrome(chrome_options=options)
    chrome_obj.delete_all_cookies()
    chrome_obj.maximize_window()
    url = "https://accounts.google.com/AccountChooser?service=mail&continue=https://mail.google.com/mail/"
    chrome_obj.get(url)

    ec_params = ['//input[@id="identifierId"]',"XPath"]
    explicit_wait(chrome_obj,"VOEL",ec_params)
    chrome_obj.find_element_by_xpath('//input[@id="identifierId"]').send_keys(email)
    chrome_obj.find_element_by_xpath('//div[@id="identifierNext"]/span/span').click()

    ec_params = ['//input[@name="password"]',"XPath"]
    explicit_wait(chrome_obj,"VOEL",ec_params)
    chrome_obj.find_element_by_xpath('//input[@name="password"]').send_keys(pwd)
    chrome_obj.find_element_by_xpath('//div[@id="passwordNext"]/span/span').click()

    try:
        #点击验证邮箱
        ec_params = ['//ul/li[1]/div/div',"XPath"]
        explicit_wait(chrome_obj,"VOEL",ec_params,timeout=5)
        chrome_obj.find_element_by_xpath('//ul/li[1]/div/div').click()
    except:
        pass

    try:
        #输入辅助邮箱
        ec_params = ['//input[@id="identifierId"]',"XPath"]
        explicit_wait(chrome_obj,"VOEL",ec_params,timeout=5)
        chrome_obj.find_element_by_xpath('//input[@id="identifierId"]').send_keys(recovery)
        chrome_obj.find_element_by_xpath('//div[1]/div[@role="button"]/span/span').click()
    except:
        pass

    #验证
    ec_params = ['//header[@role="banner"]',"XPath"]
    explicit_wait(chrome_obj,"VOEL",ec_params,timeout=60)
    l = chrome_obj.find_elements_by_xpath('//tbody/tr//div[2]/span/span')
    for email_send in l:
        email_name = email_send.text
        print(email_name)
        if email_name == "Instagram":
            email_send.click()
            ec_params = ['//div[@role="main"]',"XPath"]
            explicit_wait(chrome_obj,"VOEL",ec_params)
            chrome_obj.find_element_by_xpath('//tbody/tr[3]//tr[1]/td[2]//tr/td[2]//center/font/span').click()
            time.sleep(15)
    
    chrome_obj.quit()

if __name__ == "__main__":
    email = "gksmfsns@gmail.com"
    pwd = "7LewM7JkeEGsHde"
    recovery = "dlqhdms00@gmail.com"
    confir_gmail(email,pwd,recovery)

# 可能遇到的问题
#     浏览器不支持
#     需要验证码
#     要求更改密码