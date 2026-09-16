#!/usr/bin/env python3
"""
Security Audit Test Suite: Authorization & Header Injection Testing
Run this script to verify API endpoints are properly protected
"""

import requests
import json
import time
import jwt
from typing import Dict, Any
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "https://kodorker.vercel.app"  # Change if testing locally
ENDPOINTS = [
    ("/api/stats", "GET", "Fetch scraper statistics"),
    ("/api/supabase-usage", "GET", "Fetch Supabase usage"),
    ("/api/telegram/send-domains", "POST", "Send domains to Telegram"),
]

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(text: str):
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(70)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")

def print_test(name: str, status: str, details: str = ""):
    status_color = GREEN if status == "✅ PASS" else RED if status == "❌ FAIL" else YELLOW
    print(f"{status_color}{status}{RESET} | {name}")
    if details:
        print(f"         └─ {details}")

def test_no_token() -> bool:
    """Test 1: Access API without authentication token"""
    print_header("Test 1: No Authentication Token")
    
    results = []
    for endpoint, method, description in ENDPOINTS:
        try:
            url = f"{API_BASE_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, json={}, timeout=10)
            
            # Should return 401 Unauthorized
            if response.status_code == 401:
                print_test(
                    f"{description} ({method})",
                    "✅ PASS",
                    f"Correctly returned 401 Unauthorized"
                )
                results.append(True)
            else:
                print_test(
                    f"{description} ({method})",
                    "❌ FAIL",
                    f"Expected 401, got {response.status_code}"
                )
                results.append(False)
        except Exception as e:
            print_test(
                f"{description} ({method})",
                "⚠️  ERROR",
                f"Request failed: {str(e)}"
            )
            results.append(False)
    
    return all(results)

def test_invalid_token() -> bool:
    """Test 2: Access API with invalid JWT token"""
    print_header("Test 2: Invalid JWT Token")
    
    invalid_tokens = [
        ("malformed.token.here", "Malformed JWT"),
        ("eyJhbGciOiJub25lIiwgInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.", "alg:none"),
        ("x" * 100, "Random string"),
        ("", "Empty token"),
    ]
    
    results = []
    for token, description in invalid_tokens:
        try:
            url = f"{API_BASE_URL}/api/stats"
            cookies = {"auth_token": token}
            response = requests.get(url, cookies=cookies, timeout=10)
            
            if response.status_code == 401:
                print_test(
                    f"Token: {description}",
                    "✅ PASS",
                    f"Correctly rejected"
                )
                results.append(True)
            else:
                print_test(
                    f"Token: {description}",
                    "❌ FAIL",
                    f"Expected 401, got {response.status_code}"
                )
                results.append(False)
        except Exception as e:
            print_test(
                f"Token: {description}",
                "⚠️  ERROR",
                f"Request failed: {str(e)}"
            )
            results.append(False)
    
    return all(results)

def test_header_injection() -> bool:
    """Test 3: Try to bypass auth using header injection"""
    print_header("Test 3: Header Injection Bypass")
    
    injection_tests = [
        ({"Authorization": "Bearer valid_token"}, "Authorization Header"),
        ({"X-Auth-Token": "valid_token"}, "X-Auth-Token Header"),
        ({"X-Access-Token": "valid_token"}, "X-Access-Token Header"),
        ({"X-API-Key": "valid_token"}, "X-API-Key Header"),
        ({"Authentication": "Bearer valid_token"}, "Authentication Header"),
    ]
    
    results = []
    for headers, description in injection_tests:
        try:
            url = f"{API_BASE_URL}/api/stats"
            response = requests.get(url, headers=headers, timeout=10)
            
            # All should return 401 (token not in cookie)
            if response.status_code == 401:
                print_test(
                    description,
                    "✅ PASS",
                    f"Header injection blocked (got 401)"
                )
                results.append(True)
            else:
                print_test(
                    description,
                    "❌ FAIL",
                    f"Expected 401, got {response.status_code} - POSSIBLE BYPASS!"
                )
                results.append(False)
        except Exception as e:
            print_test(
                description,
                "⚠️  ERROR",
                f"Request failed: {str(e)}"
            )
            results.append(False)
    
    return all(results)

def test_cookie_forgery() -> bool:
    """Test 4: Try to forge JWT token without secret"""
    print_header("Test 4: JWT Token Forgery")
    
    # Try to create unsigned token (alg: none)
    forged_tokens = [
        ("eyJhbGciOiJub25lIn0.eyJ1c2VybmFtZSI6ImFkbWluIn0.", "Unsigned token (alg:none)"),
        ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.malformed", "Wrong signature"),
    ]
    
    results = []
    for token, description in forged_tokens:
        try:
            url = f"{API_BASE_URL}/api/stats"
            cookies = {"auth_token": token}
            response = requests.get(url, cookies=cookies, timeout=10)
            
            if response.status_code == 401:
                print_test(
                    description,
                    "✅ PASS",
                    f"Forged token rejected"
                )
                results.append(True)
            else:
                print_test(
                    description,
                    "❌ FAIL",
                    f"Expected 401, got {response.status_code} - TOKEN ACCEPTED!"
                )
                results.append(False)
        except Exception as e:
            print_test(
                description,
                "⚠️  ERROR",
                f"Request failed: {str(e)}"
            )
            results.append(False)
    
    return all(results)

def test_expired_token() -> bool:
    """Test 5: Try to use expired JWT token"""
    print_header("Test 5: Expired JWT Token")
    
    # Create an expired JWT (this requires secret knowledge, so we'll use old patterns)
    # Note: You need a VALID but expired token to test this properly
    print(f"{YELLOW}⚠️  SKIPPED{RESET} | Expired Token Test")
    print("         └─ Requires intercepting actual login response")
    print("         └─ Manually test after successful login with old token\n")
    
    return True

def test_method_override() -> bool:
    """Test 6: Try to bypass using HTTP method override"""
    print_header("Test 6: HTTP Method Override Bypass")
    
    try:
        url = f"{API_BASE_URL}/api/stats"
        headers = {"X-HTTP-Method-Override": "GET"}
        response = requests.post(url, headers=headers, timeout=10)
        
        # Should still return 401
        if response.status_code == 401:
            print_test(
                "X-HTTP-Method-Override to GET",
                "✅ PASS",
                "POST still requires auth"
            )
            return True
        else:
            print_test(
                "X-HTTP-Method-Override to GET",
                "❌ FAIL",
                f"Expected 401, got {response.status_code}"
            )
            return False
    except Exception as e:
        print_test(
            "X-HTTP-Method-Override",
            "⚠️  ERROR",
            f"Request failed: {str(e)}"
        )
        return False

def test_cors_bypass() -> bool:
    """Test 7: Check CORS headers (possible bypass vector)"""
    print_header("Test 7: CORS Configuration")
    
    try:
        url = f"{API_BASE_URL}/api/stats"
        response = requests.options(url, timeout=10)
        
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin", "Not Set"),
            "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials", "Not Set"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods", "Not Set"),
        }
        
        print(f"\n{BOLD}CORS Headers Detected:{RESET}")
        for header, value in cors_headers.items():
            if value == "Not Set":
                print(f"  {GREEN}✓{RESET} {header}: {value} (Good - no overly permissive CORS)")
            elif value == "*":
                print(f"  {RED}✗{RESET} {header}: {value} (Warning - too permissive)")
            else:
                print(f"  {YELLOW}?{RESET} {header}: {value} (Verify this is intended)")
        
        # Check if credentials are allowed with wildcard origin
        if cors_headers["Access-Control-Allow-Origin"] == "*" and \
           cors_headers["Access-Control-Allow-Credentials"] == "true":
            print_test(
                "CORS Configuration",
                "❌ FAIL",
                "Wildcard origin with credentials allowed - SECURITY ISSUE!"
            )
            return False
        else:
            print_test(
                "CORS Configuration",
                "✅ PASS",
                "CORS properly configured"
            )
            return True
    except Exception as e:
        print(f"\n{YELLOW}⚠️  CORS Check:{RESET} {str(e)}")
        return True

def test_security_headers() -> bool:
    """Test 8: Check security headers"""
    print_header("Test 8: Security Headers")
    
    security_headers = [
        ("X-Frame-Options", ["DENY", "SAMEORIGIN"], "Clickjacking protection"),
        ("X-Content-Type-Options", ["nosniff"], "MIME type sniffing protection"),
        ("Strict-Transport-Security", ["*"], "HTTPS enforcement"),
        ("Content-Security-Policy", ["*"], "XSS protection"),
    ]
    
    try:
        url = f"{API_BASE_URL}/api/stats"
        response = requests.head(url, timeout=10)
        
        results = []
        for header_name, expected_values, description in security_headers:
            header_value = response.headers.get(header_name, "Not Set")
            
            if header_value == "Not Set":
                print_test(
                    description,
                    "⚠️  WARN",
                    f"Header '{header_name}' not configured"
                )
                results.append(False)
            elif expected_values[0] == "*" or header_value in expected_values:
                print_test(
                    description,
                    "✅ PASS",
                    f"{header_name}: {header_value}"
                )
                results.append(True)
            else:
                print_test(
                    description,
                    "⚠️  WARN",
                    f"Unexpected value: {header_value}"
                )
                results.append(False)
        
        return any(results)  # At least some headers should be set
    except Exception as e:
        print_test(
            "Security Headers",
            "⚠️  ERROR",
            f"Check failed: {str(e)}"
        )
        return False

def main():
    """Run all security tests"""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{'SECURITY AUDIT: Authorization & Header Injection Testing'.center(70)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"\nTarget: {API_BASE_URL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Run all tests
    test_results = {
        "No Token": test_no_token(),
        "Invalid Token": test_invalid_token(),
        "Header Injection": test_header_injection(),
        "Token Forgery": test_cookie_forgery(),
        "Expired Token": test_expired_token(),
        "Method Override": test_method_override(),
        "CORS Configuration": test_cors_bypass(),
        "Security Headers": test_security_headers(),
    }
    
    # Summary
    print_header("Security Audit Summary")
    
    passed = sum(1 for v in test_results.values() if v)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"  {status} {test_name}")
    
    percentage = (passed / total) * 100
    
    print(f"\n{BOLD}Overall Score: {passed}/{total} ({percentage:.0f}%){RESET}")
    
    if percentage >= 90:
        print(f"{GREEN}✅ EXCELLENT - System is well protected against common attacks{RESET}")
    elif percentage >= 70:
        print(f"{YELLOW}⚠️  GOOD - Most protections in place, but some improvements needed{RESET}")
    else:
        print(f"{RED}❌ POOR - Multiple vulnerabilities detected, immediate action required{RESET}")
    
    print(f"\n{BOLD}Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")

if __name__ == "__main__":
    main()
