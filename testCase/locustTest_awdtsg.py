"'命令行运行locust，进行多接口事务性能测试'"

from locust import HttpUser,TaskSet,between, task ,events,SequentialTaskSet
import os,sys,json,logging,time
from readexcel import readexcel
from common.configEmail import SendEmail
from common.htmltoimage import webshot
from gevent._semaphore import Semaphore
from threading import Lock
from locust import LoadTestShape


all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()#阻塞线程
def on_hatch_complete(**kwargs):
    all_locusts_spawned.release()#释放线程

#挂到locust钩子函数  
events.spawning_complete.add_listener(on_hatch_complete)


base_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
# Domain="http://10.0.0.197"# 生产环境
Domain="http://54.187.32.55"#云测试环境


#阶梯性压测
class StagesShape(LoadTestShape):
    stages = [
        {"duration": 20, "users": 10, "spawn_rate": 5},  # 第一阶段：20秒内逐步加压到10用户
        {"duration": 40, "users": 50, "spawn_rate": 10}, # 第二阶段：40秒内加压到50用户
        {"duration": 100, "users": 100, "spawn_rate": 5} # 第三阶段：100秒内加压到100用户
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                print('当前时间为；%s,用户数：%s'%(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()),stage['users']))
                return (stage["users"], stage["spawn_rate"])
        return None


class Hellotasks(TaskSet):
    #每次在开始任务时，先执行on_start方法，只执行一次
    def on_start(self):
        print("开始执行任务")
        all_locusts_spawned.wait()#阻塞线程，直到所有locusts都被创建
        #加载excel文件数据为数组
        self.all_row_dicts = readexcel().readexcel("interfaces.xlsx")

    
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
        keywords= self.all_row_dicts[0].get('keywords')
        values= self.all_row_dicts[0].get('values')
        method= self.all_row_dicts[0].get('method')
        if values == 'None':
            values = None
        
        with self.request_method(method,url,headers,data) as response:
            print(f"请求名称: {name}")
            try:
                if response.status_code == 304:
                    response.success()
                else:
                    assert response.status_code == 200
            except AssertionError as e:
                response.failure(f"状态码非200或304,实际状态码为{response.status_code}")
            try:   
                assert json.loads(response.text).get(keywords) == values
            except AssertionError as e:
                response.failure(f"返回{keywords}不一致,期望值为{values}的类型{type(values)}，实际值为{json.loads(response.text).get(keywords)}的类型{type(json.loads(response.text).get(keywords))}")
                
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
   users = 20
   spawn_rate = 10
   run_time = "15s"
   nowtime = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
   report_path = f"{base_dir}/report/awdtsg_report{nowtime}.html"
   img_path = os.path.join(base_dir+f"/report/awdtsg_report{nowtime}.png")
   debuglog_path = os.path.join(base_dir+f"/report/awdtsg_report{nowtime}.log")
   os.system(f'/Users/admin/Documents/projects/locust/locust/.venv/bin/locust -f {__file__} --headless  --html {report_path} --logfile={debuglog_path} --loglevel=DEBUG ')
   htmlfile_path = os.path.join("file://"+report_path)
#    imgfile_path = os.path.join("/Users/admin/Documents/projects/locust/locust/testCase/report/report.jpg")  -u {users} -r {spawn_rate} -t {run_time}
   webshot(htmlfile_path,img_path)
#    SendEmail().send_attach("/results/report/report.png")
    