#!/usr/bin/env python3
"""
Security Audit Test Suite: Authorization & Header Injection Testing
Simplified version for Windows compatibility
"""

import requests
import json
from typing import Dict, Any

# Configuration
API_BASE_URL = "https://kodorker.vercel.app"

ENDPOINTS = [
    ("/api/stats", "GET", "Fetch scraper statistics"),
    ("/api/supabase-usage", "GET", "Fetch Supabase usage"),
    ("/api/telegram/send-domains", "POST", "Send domains to Telegram"),
]

print("\n" + "="*70)
print("SECURITY AUDIT: Authorization & Header Injection Testing")
print("="*70)
print(f"\nTarget: {API_BASE_URL}\n")

# Test 1: No Token
print("\n--- Test 1: No Authentication Token ---\n")
passed_count = 0
for endpoint, method, description in ENDPOINTS:
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json={}, timeout=10)
        
        if response.status_code == 401:
            print(f"[PASS] {description} ({method})")
            passed_count += 1
        else:
            print(f"[FAIL] {description} ({method}) - Got {response.status_code}, expected 401")
            print(f"       Response: {response.text[:100]}")
    except Exception as e:
        print(f"[ERROR] {description} ({method}) - {str(e)}")

print(f"\nResult: {passed_count}/3 tests passed")

# Test 2: Invalid Token
print("\n--- Test 2: Invalid JWT Token ---\n")
invalid_tokens = [
    ("malformed.token.here", "Malformed JWT"),
    ("eyJhbGciOiJub25lIiwgInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.", "alg:none"),
    ("x" * 100, "Random string"),
]

passed_count = 0
for token, description in invalid_tokens:
    try:
        url = f"{API_BASE_URL}/api/stats"
        cookies = {"auth_token": token}
        response = requests.get(url, cookies=cookies, timeout=10)
        
        if response.status_code == 401:
            print(f"[PASS] {description}")
            passed_count += 1
        else:
            print(f"[FAIL] {description} - Got {response.status_code}, expected 401")
    except Exception as e:
        print(f"[ERROR] {description} - {str(e)}")

print(f"\nResult: {passed_count}/3 tests passed")

# Test 3: Header Injection
print("\n--- Test 3: Header Injection Bypass ---\n")
injection_tests = [
    ({"Authorization": "Bearer valid_token"}, "Authorization Header"),
    ({"X-Auth-Token": "valid_token"}, "X-Auth-Token Header"),
    ({"X-Access-Token": "valid_token"}, "X-Access-Token Header"),
]

passed_count = 0
for headers, description in injection_tests:
    try:
        url = f"{API_BASE_URL}/api/stats"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 401:
            print(f"[PASS] {description} - Properly rejected")
            passed_count += 1
        else:
            print(f"[FAIL] {description} - Got {response.status_code}, BYPASS POSSIBLE!")
    except Exception as e:
        print(f"[ERROR] {description} - {str(e)}")

print(f"\nResult: {passed_count}/3 tests passed")

# Test 4: Cookie-based Authentication (should work with valid login)
print("\n--- Test 4: Valid Authentication (Check if Login Works) ---\n")
try:
    # Try login
    login_url = f"{API_BASE_URL}/api/auth/login"
    login_data = {"username": "admin", "password": "password123"}
    response = requests.post(login_url, json=login_data, timeout=10)
    
    if response.status_code == 200:
        print(f"[PASS] Login endpoint working - Status {response.status_code}")
        
        # Extract token from cookies
        cookies = response.cookies
        if 'auth_token' in cookies:
            print(f"[PASS] auth_token cookie received")
            
            # Try to use the token on protected endpoint
            stats_url = f"{API_BASE_URL}/api/stats"
            stats_response = requests.get(stats_url, cookies=cookies, timeout=10)
            
            if stats_response.status_code == 200:
                print(f"[PASS] API call with valid token - Status {stats_response.status_code}")
                print(f"       Got data: {len(stats_response.text)} bytes")
            else:
                print(f"[FAIL] API call with valid token - Got status {stats_response.status_code}")
        else:
            print(f"[FAIL] No auth_token cookie in response")
    elif response.status_code == 401:
        print(f"[INFO] Login rejected - Status 401 (credentials incorrect, but auth is working)")
    else:
        print(f"[FAIL] Login endpoint - Got status {response.status_code}")
        print(f"       Response: {response.text[:100]}")

except Exception as e:
    print(f"[ERROR] Login test - {str(e)}")

# Summary
print("\n" + "="*70)
print("SECURITY AUDIT SUMMARY")
print("="*70)
print("\n✓ API Authentication Implementation:")
print("  - No Token Test: Should return 401")
print("  - Invalid Token Test: Should return 401")
print("  - Header Injection Test: Should return 401 (headers ignored)")
print("  - Valid Token Test: Should return 200 with data")
print("\nIf all tests above show [PASS], the system is protected against:")
print("  - Unauthorized access")
print("  - Header injection attacks")
print("  - Token forgery")
print("  - Signature validation bypass")
print("\n" + "="*70 + "\n")
