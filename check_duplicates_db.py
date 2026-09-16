#!/usr/bin/env python3
"""
Check database untuk detect duplicate domains
"""

import sys
import io
from supabase import create_client
import os
from dotenv import load_dotenv
from collections import defaultdict

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

print("\n" + "="*100)
print("CHECKING DATABASE FOR DUPLICATES")
print("="*100 + "\n")

# Fetch all results
response = supabase.table("search_results").select("*").execute()
data = response.data

print(f"Total records in database: {len(data)}\n")

# Count domains
domain_count = defaultdict(list)
for record in data:
    domain = record['domain'].lower()
    domain_count[domain].append({
        'id': record['id'],
        'link': record['link'],
        'title': record['title'],
        'query': record['query'],
        'created_at': record['created_at']
    })

# Find duplicates
duplicates = {d: records for d, records in domain_count.items() if len(records) > 1}

print(f"Unique domains: {len(domain_count)}")
print(f"Duplicate domains: {len(duplicates)}\n")

if duplicates:
    print("[!] DUPLICATE DOMAINS FOUND:\n")
    for domain, records in sorted(duplicates.items()):
        print(f"  Domain: {domain} ({len(records)} records)")
        for i, record in enumerate(records):
            print(f"    [{i+1}] Link: {record['link'][:80]}...")
            print(f"        Query: {record['query']}")
            print(f"        Created: {record['created_at']}")
        print()
else:
    print("[+] NO DUPLICATE DOMAINS FOUND!")
    print(f"   All {len(domain_count)} domains are unique (1 link per domain)")

print("\n" + "="*100)

# Summary
print("\nSUMMARY:")
print(f"  Total Records: {len(data)}")
print(f"  Unique Domains: {len(domain_count)}")
print(f"  Status: {'❌ DUPLICATES DETECTED' if duplicates else '✅ CLEAN'}")
print(f"  Ratio: {len(domain_count)}/{len(data)} = {len(domain_count)/len(data)*100:.1f}% unique")

print("\n" + "="*100 + "\n")
