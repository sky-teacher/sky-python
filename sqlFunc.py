#coding utf-8
from hashlib import md5
from colorama import Fore
import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent,VERSION
from inject_class import sql_inject_payload#paylaod字典  
from color import print_colored
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service


#通过回显判断的注入测试    
def sql_back_inject(url,method,object):
    #初始化
    sql_payload=sql_inject_payload()
    #生成头
    headers={
        "User-Agent":UserAgent().random
    }
    #尝试所有注入payload
    for key,value in sql_payload.error_payload.items():
        try:
            #向url发送请求
            print(f"正在测试{object}:{key}")
            if method=="get":
                print("get请求")
                r=requests.get(url=url,params=f"{object}={value}",headers=headers)#object参数，value是payload
                print(f"{object}={value}")
            elif method=="post":
                print("post请求")
                r=requests.post(url=url,data=f"{object}={value}",headers=headers)
            else:
                print("method error")
                return
            #判断是否存在报错注入
            #判断返回的r是否有需要的MD5值
            the_str=rf"~{md5('zx'.encode('utf-8')).hexdigest()}"[:32]#因为updatxml和extractvalue的特性，报错只返回32位
            if the_str in r.text:
                payload.append(f"type:{key}\npayload:{value}")#添加payload
                print_colored(f"{key}注入成功",Fore.GREEN)
            else:
                print_colored(f"{key}注入失败",Fore.RED)  
        except:
            print_colored(f"{key}请求构造失败",Fore.RED)

    return 1        
        
#通过回显判断的注入测试    
def xss_inject(url,method,object):
    #初始化
    sql_payload=sql_inject_payload()
    #生成头
    headers={
        "User-Agent":UserAgent().random
    }
    #尝试所有注入payload
    for key,value in sql_payload.xss_payload.items():
        # 创建 WebDriver 对象，指明使用edge浏览器驱动
        # 启动浏览器
        options = Options()#定义一个option对象
        options.add_argument("headless")#实现无可视化界面的操作,无可视化界面（无头浏览器）提高效率
        service = Service(executable_path=r'msedgedriver.exe')
        driver = webdriver.Edge(service=service,options=options)
        if method =="get":
            try:
                # 打开网页
                if "?" in url:#说明有参数，新参数加&
                    mypayload=f"&{object}={value}"
                else:#没有参数，新参数加？
                    mypayload=f"?{object}={value}"
                driver.get(url+mypayload)#访问带参数的页面
            
                # 循环处理弹窗
                while True:
                        # 切换到当前弹窗
                        try:
                            alert = Alert(driver)  
                            # 例如检查文本内容是否存在我们要的值
                            if f"{md5('zx'.encode('utf-8')).hexdigest()}" in alert.text:
                                print_colored(f"{key}注入成功",Fore.GREEN)
                                payload.append(f"type:{key}\npayload:{value}")#添加payload
                            else:
                                print_colored(f"{key}注入失败",Fore.RED)
                            # 处理完弹窗后关闭
                            alert.accept()
                        except:
                            break#弹窗检测完毕  
            finally:
                # 关闭浏览器
                driver.quit()

    return 1        


def sql_inject(url,method,object):#对传入的数据进行对应检测
    global payload
    payload=[]
    sql_back_inject(url,method,object)#返回成功payload列表
    xss_inject(url,method,object)#测试xss
    return payload


