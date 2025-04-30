"'命令行运行locust，进行多接口事务性能测试'"

from locust import HttpUser,TaskSet,between, task 
import os,sys,json,logging,requests
from readexcel import readexcel

#将引入内部文件所在目录加进sys.path中
base_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
from common.configEmail import SendEmail
from common.htmltoimage import webshot

#v1.0以上版本没有httplocust(The HttpLocust class has been renamed to HttpUser in version 1.0)
# 定义用户行为，继承TaskSet类，用于描述用户行为
# (这个类下面放各种请求，请求是基于requests的，每个方法请求和requests差不多，请求参数、方法、响应对象和requests一样的使用，url这里写的是路径)
class Hellotasks():
    
    def __init__(self):
        self.all_row_dicts = readexcel().all_row_dict

    def test_list(self):
        headers = {}
        try:
            headers = self.all_row_dicts[0].get('header')
            headers = json.loads(headers)
            # # 检查 headers 是否为字典类型  
            # if not isinstance(headers, dict):
            #     raise ValueError("headers 不是字典类型")
        except json.JSONDecodeError as e:
            print(f"解析 header 数据失败: {e}")
            print(f"原始 header 数据: {self.all_row_dicts[0].get('header')}")  
            headers = {}
        name = self.all_row_dicts[0].get('name')
        url = self.all_row_dicts[0].get('url')
        data= self.all_row_dicts[0].get('data')
        code= self.all_row_dicts[0].get('code')
        msg= self.all_row_dicts[0].get('msg')
        
        try:
            r = requests.post(url, timeout=60, headers=headers,json=json.loads(data))
            print(f"请求名称: {name}")
            assert r.status_code == 200
            assert json.loads(r.text).get('code') == code
            assert json.loads(r.text).get('msg') == msg
        except Exception as e:
            logging.exception(f"请求失败: {e}")
            logging.error(f"请求失败: {e}")
            logging.error(f"请求头: {headers}")
            logging.error(f"请求数据: {data}")



if __name__=='__main__':
 
    
   test=Hellotasks()
   test.test_list()