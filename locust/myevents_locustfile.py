from locust import HttpUser, task, between

class MyEventsUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.post("/login", data={"username": "tester", "password": "tester123"})

    @task
    def view_my_events(self):
        self.client.get("/my-events")
