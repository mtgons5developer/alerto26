from locust import HttpUser, task, between
import random

class EmergencyUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(3)
    def view_emergencies(self):
        query = {"query": "{ emergencies { id emergencyType status } }"}
        self.client.post("/graphql/", json=query)
    
    @task(1)
    def create_emergency(self):
        mutation = {
            "query": """
            mutation {
              createEmergency(
                emergencyType: "MEDICAL"
                latitude: %.6f
                longitude: %.6f
              ) {
                emergency { id code }
              }
            }
            """ % (random.uniform(40.7, 40.8), random.uniform(-74.1, -73.9))
        }
        self.client.post("/graphql/", json=mutation)
    
    @task(2)
    def health_check(self):
        self.client.get("/health/")
