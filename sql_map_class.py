#coding utf-8
from colorama import Fore
import sqlFunc#sql注入函数
import re
from color import print_colored

class sql_map_class():
    url='www.baidu.com'
    object=[]
    method='get'
    __payload={}
    def __init__(self,url,method,*object):#初始化其中obbject为元组可接收多个参数
        if not re.fullmatch(r'^(post|get)$',method):
            raise Exception('method参数错误')
        self.url=url
        self.object=object
        self.method=method
    
    def test_sql_inject(self):
        for i in self.object: #每一个参数都进行测试
            print_colored(i,Fore.YELLOW)
            payload=sqlFunc.sql_inject(self.url,self.method,i)
            if payload != []:
                if i not in self.__payload:
                    self.__payload[f'{i}']=[]
                self.__payload[f'{i}'].append(payload)#将对应的payload放入字典对应的键值中
            else:
                if i not in self.__payload:
                   self.__payload[f'{i}']=[]
                self.__payload[f'{i}'].append("无有效payload")    
    def get_payload(self):
        sql_list = []
        for key,value in self.__payload.items():
            for list_value in value:
                for i in list_value:
                    sql_list.append(f"url:{self.url}\n请求:{self.method},参数:{key}\n{i}")

        return sql_list