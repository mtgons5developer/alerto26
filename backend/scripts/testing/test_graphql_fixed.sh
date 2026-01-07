#!/bin/bash
echo "🔍 Testing GraphQL with trailing slash fix..."

# Test with slash
echo "1. Testing /graphql/ (with slash):"
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __typename }"}' \
  -w "\nStatus: %{http_code}\n"

echo -e "\n2. Testing /graphql (no slash):"
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __typename }"}' \
  -w "\nStatus: %{http_code}\n"

echo -e "\n3. Testing actual query:"
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ emergencies { id emergencyType } }"}' \
  -s | python3 -m json.tool | head -20
