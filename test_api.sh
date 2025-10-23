#!/bin/bash

echo "🧪 Testing Abalone Age Prediction API"
echo "===================================="

API_URL="http://localhost:8000"

# Test health endpoint
echo "1. Testing health endpoint..."
curl -s "$API_URL/health" | jq . 2>/dev/null || curl -s "$API_URL/health"
echo ""

# Test model info
echo "2. Testing model info..."
curl -s "$API_URL/model/info" | jq . 2>/dev/null || curl -s "$API_URL/model/info"
echo ""

# Test prediction
echo "3. Testing prediction..."
curl -X POST "$API_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
  }' | jq . 2>/dev/null || curl -X POST "$API_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
  }'

echo ""
echo "✅ API tests completed!"
