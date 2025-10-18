#!/usr/bin/env python3
"""
Test script for web search and AI research features
Tests the new endpoints without requiring the full AI model to be loaded
"""

import requests
import json
from ddgs import DDGS
import sys

def test_duckduckgo_search():
    """Test if DuckDuckGo search is working"""
    print("=" * 60)
    print("Testing DuckDuckGo Search Library")
    print("=" * 60)
    
    try:
        query = "Python programming tutorial"
        print(f"\nSearching for: '{query}'")
        
        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, max_results=3):
                results.append({
                    'title': r.get('title', ''),
                    'link': r.get('href', ''),
                    'snippet': r.get('body', '')
                })
        
        print(f"✓ Found {len(results)} results")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   {result['link']}")
            print(f"   {result['snippet'][:100]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_search_endpoint(base_url="http://localhost:5000"):
    """Test the /search endpoint"""
    print("\n" + "=" * 60)
    print("Testing /search Endpoint")
    print("=" * 60)
    
    try:
        query = "artificial intelligence news"
        print(f"\nSending request to {base_url}/search")
        print(f"Query: '{query}'")
        
        response = requests.post(
            f"{base_url}/search",
            json={"query": query, "max_results": 3},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Found {data['count']} results")
            
            for i, result in enumerate(data['results'], 1):
                print(f"\n{i}. {result['title']}")
                print(f"   {result['link']}")
            
            return True
        else:
            print(f"✗ Status: {response.status_code}")
            print(f"✗ Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server")
        print("  Make sure the server is running at", base_url)
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_health_endpoint(base_url="http://localhost:5000"):
    """Test the /health endpoint"""
    print("\n" + "=" * 60)
    print("Testing /health Endpoint")
    print("=" * 60)
    
    try:
        print(f"\nSending request to {base_url}/health")
        
        response = requests.get(f"{base_url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Server Status: {data.get('status', 'unknown')}")
            print(f"✓ Model Loaded: {data.get('model_loaded', False)}")
            print(f"✓ Device: {data.get('device', 'unknown')}")
            return True
        else:
            print(f"✗ Status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server")
        print("  Make sure the server is running at", base_url)
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_config_endpoint(base_url="http://localhost:5000"):
    """Test the /config endpoint"""
    print("\n" + "=" * 60)
    print("Testing /config Endpoint")
    print("=" * 60)
    
    try:
        print(f"\nSending request to {base_url}/config")
        
        response = requests.get(f"{base_url}/config", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Model: {data.get('model_name', 'unknown')}")
            print(f"✓ Device: {data.get('device', 'unknown')}")
            print(f"✓ Model Loaded: {data.get('model_loaded', False)}")
            print(f"✓ CUDA Available: {data.get('cuda_available', False)}")
            return True
        else:
            print(f"✗ Status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server")
        print("  Make sure the server is running at", base_url)
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_home_endpoint(base_url="http://localhost:5000"):
    """Test the / endpoint (API mode)"""
    print("\n" + "=" * 60)
    print("Testing / Endpoint (API Mode)")
    print("=" * 60)
    
    try:
        print(f"\nSending request to {base_url}/")
        
        response = requests.get(
            f"{base_url}/",
            headers={"Accept": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Server: {data.get('name', 'unknown')}")
            print(f"✓ Version: {data.get('version', 'unknown')}")
            print(f"✓ Features: {', '.join(data.get('features', []))}")
            print(f"✓ Endpoints: {len(data.get('endpoints', {}))} available")
            return True
        else:
            print(f"✗ Status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server")
        print("  Make sure the server is running at", base_url)
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def run_all_tests(base_url="http://localhost:5000"):
    """Run all tests"""
    print("\n" + "=" * 60)
    print("LOCAL AI SERVER - WEB SEARCH FEATURE TESTS")
    print("=" * 60)
    print(f"\nServer URL: {base_url}")
    print("\nNote: Some tests require the server to be running.")
    print("To start the server: cd local_ai_server && python ai_server.py")
    
    results = {
        "DuckDuckGo Search": test_duckduckgo_search(),
        "Home Endpoint": test_home_endpoint(base_url),
        "Health Endpoint": test_health_endpoint(base_url),
        "Config Endpoint": test_config_endpoint(base_url),
        "Search Endpoint": test_search_endpoint(base_url)
    }
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:30} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print("\n" + "-" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    # Allow custom server URL
    server_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    success = run_all_tests(server_url)
    
    if success:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed. Check output above for details.")
        print("\nTroubleshooting:")
        print("1. Make sure the server is running: python ai_server.py")
        print("2. Check if dependencies are installed: pip install -r requirements.txt")
        print("3. Verify internet connection for web search tests")
        sys.exit(1)
