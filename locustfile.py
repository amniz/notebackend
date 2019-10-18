from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        self.client.post("/",{"username":"nzm","password":"123"})

    @task(1)
    def Note(self):
        self.client.get("/Note")




class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 2000