#!/usr/bin/env python3
"""
Test script for the AI server
"""

import requests
import json

def test_server(base_url):
    """Test the AI server endpoints"""
    
    print(f"Testing server at: {base_url}")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test models endpoint
    print("\n2. Testing /models endpoint...")
    try:
        response = requests.get(f"{base_url}/models")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test chat endpoint
    print("\n3. Testing /chat endpoint...")
    try:
        data = {
            "message": "Hello! Tell me a joke.",
            "max_length": 100,
            "temperature": 0.7
        }
        response = requests.post(
            f"{base_url}/chat",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("Testing complete!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Try to read from ngrok_url.txt
        try:
            with open('ngrok_url.txt', 'r') as f:
                url = f.read().strip()
            print(f"Using URL from ngrok_url.txt: {url}")
        except:
            url = "http://localhost:5000"
            print(f"Using default URL: {url}")
    
    test_server(url)
