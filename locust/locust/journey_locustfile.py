from locust import HttpUser, task, between

class FestJourneyUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.post("/login", data={"username": "tester", "password": "tester123"})

    @task
    def journey(self):
        self.client.get("/events")
        self.client.get("/events/1/register")
        self.client.get("/my-events")
        self.client.get("/checkout")
