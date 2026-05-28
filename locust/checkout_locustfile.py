from locust import HttpUser, task, between

class CheckoutUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.post("/login", data={"username": "tester", "password": "tester123"})

    @task
    def checkout(self):
        self.client.get("/checkout")
