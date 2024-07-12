#coding utf-8
from colorama import Fore
from sql_map_class import sql_map_class#大类
import sys
from color import print_colored

if __name__ == '__main__':
    print("开始初始化")
    #初始化
    try:
        #如果有必传的定值参数请写在url之中
        sql_map=sql_map_class("http://www.pikachu.com/vul/sqli/sqli_str.php?submit='查询'","get","name")#url,object,method 网站地址，检测对象，请求方式(默认get)
    except Exception as e:
        print(e)
        print("请输入正确参数：python3 sqlmap.py url object method")
        exit()
    print("开始检测")
    #开始检测
    try:
        sql_map.test_sql_inject()
    except Exception as e:
        print(e)
        exit()
    #打印结果S
    print("打印结果")
    try:
        for i in sql_map.get_payload():
            print_colored("--------------------------------------------------")
            print_colored(i,Fore.YELLOW)
            print_colored("--------------------------------------------------")
    except Exception as e:
        print(e)
        exit()   
