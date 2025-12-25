"""
Test script for parcel search API
"""
import requests
import json

API_URL = "http://localhost:8000/api/v1/parcels/search"

# Test 1: İl ile arama
print("Test 1: İl ile arama (Ankara)")
response = requests.post(API_URL, json={"province": "Ankara"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
print()

# Test 2: İlçe ile arama
print("Test 2: İlçe ile arama (Çankaya)")
response = requests.post(API_URL, json={"district": "Çankaya"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
print()

# Test 3: Ada ile arama
print("Test 3: Ada ile arama (123)")
response = requests.post(API_URL, json={"block": "123"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
print()

# Test 4: Parsel ile arama
print("Test 4: Parsel ile arama (456)")
response = requests.post(API_URL, json={"parcel_number": "456"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
print()

# Test 5: Boş arama
print("Test 5: Boş arama (tüm parseller)")
response = requests.post(API_URL, json={})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
print()

