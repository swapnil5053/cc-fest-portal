from locust import HttpUser, task, between

class EventsUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.post("/login", data={"username": "tester", "password": "tester123"})

    @task(3)
    def browse_events(self):
        self.client.get("/events")

    @task(1)
    def search_events(self):
        self.client.get("/events?q=workshop")
