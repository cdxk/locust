"'命令行运行locust，进行多接口事务性能测试'"

from locust import HttpUser,TaskSet,task,between
import os,sys
from readexcel import readexcel

#将引入内部文件所在目录加进sys.path中
base_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
from common.configEmail import SendEmail
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
        # 将字符串强制转化为字典
        header = eval(self.all_row_dicts[0].get('header'))
        name = self.all_row_dicts[0].get('name')
        url = self.all_row_dicts[0].get('url')
        r = self.client.post(url, timeout=60, headers=header)
        assert r.status_code == 200


    @task(2)
    def test_detail(self):
        header = eval(self.all_row_dicts[1].get('header'))
        name = self.all_row_dicts[1].get('name')
        url = self.all_row_dicts[1].get('url')
        r = self.client.post(url, timeout=60, headers=header)
        assert r.status_code == 200

class HelloWorld(HttpUser):
    wait_time = between(1, 5)
    tasks=[Hellotasks]


if __name__=='__main__':
    #获取当前文件的绝对路径
    # file_name=os.path.abspath(__file__)
    # print(file_name)
    # os.system(f'/Users/caidan/venv/interfaceAuto/bin/locust -f {file_name} -u 4 -r 2 -t 10s')
    os.system(f'/Users/caidan/venv/interfaceAuto/bin/locust -f /Users/caidan/tool/cai/pycharmProject/locust/testCase/locustTest.py --headless -H https://crmtest.gaker.com --u 2 -r2 -t 10s --html /Users/caidan/tool/cai/pycharmProject/locust/testCase/report/report.html')
    SendEmail().send_attach('/testCase/report/report.html')