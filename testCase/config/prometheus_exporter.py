from locust import events
from prometheus_client import start_http_server, Counter, Gauge, Histogram

# 定义Prometheus指标
REQUEST_RPS = Counter('locust_requests_total', 'Total requests per second')
RESPONSE_TIME = Histogram('locust_response_time_seconds', 'Response time distribution')
FAILED_REQUESTS = Counter('locust_failed_requests_total', 'Total failed requests')
USERS_COUNT = Gauge('locust_users_current', 'Current number of active users')

# 启动Prometheus metrics服务器（默认端口8000）
start_http_server(8000)

# Locust事件钩子
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    REQUEST_RPS.inc()
    RESPONSE_TIME.observe(response_time / 1000)  # 转换为秒
    if exception:
        FAILED_REQUESTS.inc()

@events.test_start.add_listener
def on_test_start(**kwargs):
    USERS_COUNT.set(0)  # 重置用户数

@events.user_spawn.add_listener
def on_user_spawn(user_count, **kwargs):
    USERS_COUNT.set(user_count)
