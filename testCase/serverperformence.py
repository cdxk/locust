# from locust import HttpUser, task, between
# from locust_plugins import ResourceMonitor

# class MyUser(HttpUser):
#     wait_time = between(1, 3)

#     @task
#     def my_task(self):
#         self.client.get("https://www.baidu.com")

# # 启动资源监控（默认采集本机指标）
# # ResourceMonitor()  # 默认监控CPU、内存、磁盘IO

# resour_monitor=ResourceMonitor(
#     targets=[
#         "cpu",          # CPU使用率
#         "mem",          # 内存占用
#         "disk/read",    # 磁盘读取速率
#         "disk/write",   # 磁盘写入速率
#         "network"       # 网络流量
#     ],
#     sample_rate=2      # 采样频率（秒）
# )
# resour_monitor.start()  # 启动资源监控

import psutil
import paramiko
from datetime import datetime
import time
import csv

# def monitor_resources():
#     print(f"CPU使用率: {psutil.cpu_percent()}%")
#     print(f"内存占用: {psutil.virtual_memory().percent}%")
#     print(f"磁盘读取速率: {psutil.disk_io_counters().read_bytes} bytes")
#     print(f"磁盘写入速率: {psutil.disk_io_counters().write_bytes} bytes")
#     print(f"网络流量: {psutil.net_io_counters().bytes_sent} bytes sent, {psutil.net_io_counters().bytes_recv} bytes received")

# monitor_resources()

def get_remote_stats(host, user, password,port=22):
    #创建SSH连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动信任新主机:ml-citation{ref="2,3" data="citationList"}
    try:
        ssh.connect(host, port, user, password)
        print(f"成功连接到 {host}")
    except Exception as e:
        print(f"连接失败: {str(e)}")
    
    # 执行远程命令获取指标
    # stdin, stdout, stderr = ssh.exec_command('python3 -c "import psutil; print(psutil.cpu_percent(), psutil.virtual_memory().percent, psutil.disk_usage(\'/\').percent, psutil.net_io_counters().bytes_sent, psutil.net_io_counters().bytes_recv)"')
    stdin, stdout, stderr = ssh.exec_command('python3 -c "import psutil; print(psutil.cpu_percent(interval=1), flush=True)"')
  
    output=stdout.read().decode().strip()
    error=stderr.read().decode().strip()
    if error:
        #如果被监控服务器没有安装python 和psutil模块，则需要安装
        print(f"远程命令执行失败: {error}") 
        return None
    if not output:
        print(f"远程命令未返回任何数据，主机: {host}")
        return None
    try:
        cpu, mem, disk, net_sent, net_recv = map(float, stdout.split())
        return {
        'host': host,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_usage': cpu,
        'mem_usage': mem,
        'disk_usage': disk,
        'net_sent': net_sent,  # 网络上行单位：字节
        'net_recv': net_recv   # 网络下行单位：字节
        }
    except ValueError as e:
        print(f"解析远程命令输出失败: {output}, 错误: {e}")
        return None
        
        
    # 解析结果
    
# 监控多台主机
def monitor(filepath,hosts, interval=60):
    with open(filepath, 'a') as f:
        while True:
            for host in hosts:
                metrics = get_remote_stats(
                host['ip'], 
                host['user'], 
                host['password'],
                host['port']
                )
                if metrics is None:
                    print(f"获取指标失败，主机: {host['ip']}")
                    continue
                writer = csv.DictWriter(f, fieldnames=metrics.keys())
                if f.tell() == 0:  # 文件为空时写入表头
                    writer.writeheader()
                writer.writerow(metrics)
                # print(f"[{metrics['timestamp']}] {host['ip']} - CPU: {metrics['cpu_usage']}%")
            time.sleep(interval) #每60秒采集一次数据

        
if __name__ == "__main__":
    hosts = [
    {'ip': '10.0.0.197', 'user': 'root', 'password': '123456', 'port': 22},
    ]
    filepath = 'performance_metrics.csv'
        
    monitor(filepath,hosts, interval=60)