#!/bin/bash
# Quick test script for the AI server

URL="https://unpredestined-callow-cortney.ngrok-free.dev"

echo "🧪 Testing AI Server..."
echo "URL: $URL"
echo ""

echo "1️⃣ Testing /health endpoint..."
curl -s "$URL/health" | python3 -m json.tool
echo ""
echo ""

echo "2️⃣ Testing /models endpoint..."
curl -s "$URL/models" | python3 -m json.tool
echo ""
echo ""

echo "3️⃣ Testing /chat endpoint..."
curl -X POST "$URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello! Tell me a joke.","max_length":100}' \
  | python3 -m json.tool

echo ""
echo "✅ Test complete!"
