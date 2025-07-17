from locust import HttpUser, task, between
import json
import random

class CostTrackerUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Setup for each user"""
        self.api_key = "your-api-key"
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        
        # Test data
        self.services = ["EC2", "S3", "Lambda", "DynamoDB", "RDS"]
        self.clients = ["production", "staging", "development", "testing"]
    
    @task(3)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/health")
    
    @task(5)
    def create_expense(self):
        """Test creating expenses"""
        expense_data = {
            "service_name": random.choice(self.services),
            "client": random.choice(self.clients),
            "cost": round(random.uniform(1.0, 1000.0), 2),
            "description": f"Test expense {random.randint(1, 1000)}"
        }
        
        response = self.client.post(
            "/expenses",
            headers=self.headers,
            data=json.dumps(expense_data)
        )
        
        if response.status_code == 201:
            # Store expense ID for later use
            expense_id = response.json().get("expense_id")
            if expense_id:
                self.expense_id = expense_id
    
    @task(2)
    def get_expenses(self):
        """Test listing expenses"""
        self.client.get("/expenses", headers=self.headers)
    
    @task(1)
    def get_cost_breakdown(self):
        """Test cost breakdown endpoint"""
        self.client.get("/cost-breakdown", headers=self.headers)
    
    @task(1)
    def get_monthly_trends(self):
        """Test monthly trends endpoint"""
        self.client.get("/monthly-trends", headers=self.headers)
