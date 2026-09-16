#!/usr/bin/env python3
"""
Delete duplicate domains - Keep only the OLDEST record per domain
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
print("CLEANUP DUPLICATE DOMAINS - Keep OLDEST record per domain")
print("="*100 + "\n")

# Fetch all results
response = supabase.table("search_results").select("*").execute()
data = response.data

print(f"[*] Total records: {len(data)}\n")

# Group by domain and sort by created_at
domain_groups = defaultdict(list)
for record in data:
    domain = record['domain'].lower()
    domain_groups[domain].append({
        'id': record['id'],
        'link': record['link'],
        'created_at': record['created_at']
    })

# Find duplicates and mark for deletion (keep oldest)
to_delete = []
for domain, records in domain_groups.items():
    if len(records) > 1:
        # Sort by created_at (oldest first)
        sorted_records = sorted(records, key=lambda x: x['created_at'])
        # Keep oldest, delete rest
        for record in sorted_records[1:]:
            to_delete.append(record['id'])

print(f"[*] Found {len(to_delete)} records to delete")
print(f"[*] Will keep {len(data) - len(to_delete)} records\n")

if not to_delete:
    print("[+] No duplicates found!")
    exit(0)

# Confirm before delete
print("[!] Preview of records to delete:")
count = 0
for record in data:
    if record['id'] in to_delete:
        print(f"    ID: {record['id']} | Domain: {record['domain']} | Link: {record['link'][:60]}...")
        count += 1
        if count >= 10:
            print(f"    ... dan {len(to_delete) - 10} record lainnya")
            break

response = input("\n[?] Delete these records? (type 'yes' to confirm): ").strip().lower()
if response != 'yes':
    print("[-] Aborted!")
    exit(0)

# Delete records
print(f"\n[*] Deleting {len(to_delete)} records...")
deleted_count = 0

for record_id in to_delete:
    try:
        supabase.table("search_results").delete().eq("id", record_id).execute()
        deleted_count += 1
    except Exception as e:
        print(f"[-] Error deleting ID {record_id}: {e}")

print(f"\n[+] Successfully deleted {deleted_count} records!")
print(f"[+] Remaining records: {len(data) - deleted_count}")
print(f"\n" + "="*100)
print("CLEANUP COMPLETE")
print("="*100 + "\n")
