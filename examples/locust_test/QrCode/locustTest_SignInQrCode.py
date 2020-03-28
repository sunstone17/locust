import random
import uuid

from locust import HttpLocust, TaskSet, task, between


class PerformanceTest(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.actionIds = []
        with open('./data/Nos.txt', 'r') as f:
            self.Nos = f.readlines()
            self.NosCount = len(self.Nos)

    def setup(self):
        # 如果后台需要的是json格式，需要加header，否则报415
        header = {"Content-Type": "application/json"}
        self.client.headers.update(header)
        
    def on_stop(self):
        with open('./data/actionIds.txt', 'a') as f:
            for actionId in self.actionIds:
                f.write(actionId + "\n")

    @task
    def index(self):
        actionId = str(uuid.uuid4())
        num = self.Nos[random.randint(0, self.NosCount - 1)][0:-1]
        payload = {
            'actionId': actionId,
            }
        }
        print(payload)
        with self.client.post('接口2', json=payload, name='接口2',catch_response=True) as response:
            self.actionIds.append(actionId)
            print(response.content)


class PerformanceTestUser(HttpLocust):
    host = "http://localhost:10001"
    task_set = PerformanceTest
    wait_time = between(5, 15)

# cd C:\DEV\MS\Python\PyDev
# locust -f locustTest.py 
# http://localhost:8089/
# Numberof users to simulate:设置虚拟用户数
# Hatch rate (users spawned/second): 每秒产生的用户数
# Host
