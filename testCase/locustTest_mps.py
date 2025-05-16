"'命令行运行locust，进行多接口事务性能测试'"

from locust import HttpUser,TaskSet,between, task 
import os,sys,json,logging
from readexcel import readexcel
from common.configEmail import SendEmail
from common.htmltoimage import webshot



base_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
Domain="https://mps.lollicupdev.com"
# 定义用户行为，继承TaskSet类，用于描述用户行为
class Hellotasks(TaskSet):
    #每次在开始任务时，先执行on_start方法，只执行一次
    def on_start(self):
        #加载excel文件数据为数组
        self.all_row_dicts = readexcel().readexcel("interfacesmps.xlsx")
    
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
        url = Domain+self.all_row_dicts[0].get('url')
        data= self.all_row_dicts[0].get('data')
        code= self.all_row_dicts[0].get('code')
        msg= self.all_row_dicts[0].get('msg')
        method= self.all_row_dicts[0].get('method')
        
        with self.request_method(method,url,headers,data) as response:
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
                
    def request_method(self, method,url, headers=None, data=None):
        if method == 'get':
            return self.client.get(url, timeout=60, headers=headers,catch_response=True)
        elif method == 'post':
            return self.client.post(url, timeout=60, headers=headers,json=json.loads(data),catch_response=True)
        else:
            raise ValueError(f"不支持的请求方法: {method}")


            

class HelloWorld(HttpUser):
    wait_time = between(1, 5)
    tasks=[Hellotasks]
    host = Domain


if __name__=='__main__':
   users = 2
   spawn_rate = 2
   run_time = "5s"
   report_path = f"{base_dir}/report/Mpsreport.html"
   img_path = os.path.join(base_dir+"/report/Mpsreport.png")
   os.system(f'/Users/admin/Documents/projects/locust/locust/.venv/bin/locust -f {__file__} --headless -u {users} -r {spawn_rate} -t {run_time} --html {report_path} ')
   htmlfile_path = os.path.join("file://"+report_path)
#    imgfile_path = os.path.join("/Users/admin/Documents/projects/locust/locust/testCase/report/report.jpg")
   webshot(htmlfile_path,img_path)
#    SendEmail().send_attach("/results/report/report.png")
    