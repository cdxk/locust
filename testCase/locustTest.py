"'命令行运行locust，进行多接口事务性能测试'"

from locust import HttpUser,TaskSet,between, task 
import os,sys,json,logging
from readexcel import readexcel

#将引入内部文件所在目录加进sys.path中
base_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
from common.configEmail import SendEmail
from common.htmltoimage import webshot

#v1.0以上版本没有httplocust(The HttpLocust class has been renamed to HttpUser in version 1.0)
# 定义用户行为，继承TaskSet类，用于描述用户行为
# (这个类下面放各种请求，请求是基于requests的，每个方法请求和requests差不多，请求参数、方法、响应对象和requests一样的使用，url这里写的是路径)
class Hellotasks(TaskSet):
    #每次在开始任务时，先执行on_start方法，只执行一次
    def on_start(self):
        #加载excel文件数据为数组
        self.all_row_dicts = readexcel().all_row_dict
    # task装饰该方法为一个事务方法的参数用于指定该行为的执行权重。参数越大，每次被虚拟用户执行概率越高，不设置默认是1，
    @task(1)
    def test_list(self):
        headers = {}
        try:
            headers = self.all_row_dicts[0].get('header')
            headers = json.loads(headers)
        except json.JSONDecodeError as e:
            print(f"解析 header 数据失败: {e}")
            print(f"原始 header 数据: {self.all_row_dicts[0].get('header')}")  
            headers = {}
        name = self.all_row_dicts[0].get('name')
        url = self.all_row_dicts[0].get('url')
        data= self.all_row_dicts[0].get('data')
        code= self.all_row_dicts[0].get('code')
        msg= self.all_row_dicts[0].get('msg')
        
        with self.client.post(url, timeout=60, headers=headers,json=json.loads(data),catch_response=True) as response:
            print(f"请求名称: {name}")
            try:
                assert response.status_code == 200
            except AssertionError as e:
                response.failure(f"状态码非200")
            try:
                assert json.loads(response.text).get('code') == code
            except AssertionError as e: 
                response.failure(f"返回code不一致")
            try:   
                assert json.loads(response.text).get('msg') == msg
            except AssertionError as e:
                response.failure(f"返回msg不一致")

class HelloWorld(HttpUser):
    wait_time = between(1, 5)
    tasks=[Hellotasks]


if __name__=='__main__':
   users = 2
   spawn_rate = 2
   run_time = "10s"
   report_path = "/Users/admin/Documents/projects/locust/locust/testCase/report/report2.html"
   os.system(f'/Users/admin/Documents/projects/locust/locust/.venv/bin/locust -f {__file__} --headless -H https://mps.lollicupdev.com -u {users} -r {spawn_rate} -t {run_time} --html {report_path} ')
   htmlfile_path = os.path.join("file://"+base_dir+"/testCase/report/report2.html")
#    imgfile_path = os.path.join("/Users/admin/Documents/projects/locust/locust/testCase/report/report.jpg")
   webshot(htmlfile_path)
    # SendEmail().send_attach( )
    