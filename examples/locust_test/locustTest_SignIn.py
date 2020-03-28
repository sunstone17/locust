import random
from locust import HttpLocust, TaskSet, task, between


class PerformanceTest(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        with open('./signInData/actionIds.txt', 'r') as f:
            self.actionIds = f.readlines()
            self.actionIdsCount = len(self.actionIds)

        with open('./signInData/openIds.txt', 'r') as f:
            self.openIds = f.readlines()
            self.openIdsCount = len(self.openIds)

    def setup(self):
        # 如果后台需要的是json格式，需要加header，否则报415
        headers = {"Content-Type": "application/json", "Authorization": ""}
        self.client.headers.update(headers)

    @task
    def index(self):

        actionId = self.actionIds[random.randint(0, self.actionIdsCount - 1)][0:-1]
        openId = self.openIds[random.randint(0, self.openIdsCount - 1)][0:-1]
        print('actionId\n' + actionId + '\nopenId\n' + openId)

        with self.client.post('address?para1='+actionId, name='接口1', catch_response=True) as response:
            print(response.content.decode('utf-8', errors='ignore'))


class PerformanceTestUser(HttpLocust):
    host = ""
    task_set = PerformanceTest
    wait_time = between(5, 15)

# cd C:\DEV\MS\Python\PyDev
# locust -f locustTest.py 
# http://localhost:8089/
# Numberof users to simulate:设置虚拟用户数
# Hatch rate (users spawned/second): 每秒产生的用户数
# Host
