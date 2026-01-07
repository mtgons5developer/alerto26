# scripts/testing/graphql_client.py
import requests

class GraphQLClient:
    def __init__(self, endpoint="http://localhost:8000/graphql/"):
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json"}
    
    def query(self, query, variables=None):
        """Execute GraphQL query"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        response = requests.post(
            self.endpoint,
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    def mutate(self, mutation, variables=None):
        """Execute GraphQL mutation"""
        return self.query(mutation, variables)

# Usage:
from graphql_client import GraphQLClient

client = GraphQLClient()
result = client.query("{ emergencies { id code } }")
print(result)