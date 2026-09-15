#!/usr/bin/env python3
"""
Delete duplicates using raw SQL via Supabase admin API
Requires SUPABASE_SERVICE_ROLE_KEY for bypassing RLS
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
admin_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not admin_key:
    print("❌ SUPABASE_SERVICE_ROLE_KEY not found in .env")
    print("Need to:")
    print("  1. Go to Supabase dashboard")
    print("  2. Project Settings → API Keys")
    print("  3. Copy 'service_role' key")
    print("  4. Add to .env: SUPABASE_SERVICE_ROLE_KEY=<your_key>")
    print("\nAlternatively, delete manually via:")
    print("  - Supabase Dashboard → SQL Editor")
    print("  - Run: DELETE FROM search_results WHERE id IN (...list of duplicate IDs...)")
    exit(1)

print("\n" + "="*100)
print("DELETE DUPLICATES VIA SQL (Admin Access)")
print("="*100 + "\n")

# SQL to identify and delete duplicates
# Keep most recent record per domain
sql = """
WITH duplicates AS (
  SELECT id, domain, 
    ROW_NUMBER() OVER (PARTITION BY LOWER(domain) ORDER BY created_at DESC) as rn
  FROM search_results
)
DELETE FROM search_results 
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1)
RETURNING id, domain;
"""

headers = {
    "apikey": admin_key,
    "Authorization": f"Bearer {admin_key}",
    "Content-Type": "application/json"
}

print(f"Executing SQL (with admin key)...\n")

response = requests.post(
    f"{url}/rest/v1/rpc/exec",
    headers=headers,
    json={"sql": sql}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

if response.status_code == 200:
    print("\n✅ SQL executed successfully!")
else:
    print(f"\n❌ Error: {response.status_code}")

print("\n" + "="*100)
