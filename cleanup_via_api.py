#!/usr/bin/env python3
"""
Delete duplicates via Supabase REST API with proper headers
"""

import requests
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print("\n" + "="*100)
print("DATABASE CLEANUP: Via REST API")
print("="*100 + "\n")

# Fetch all results using REST API
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

print("Fetching all records...")
response = requests.get(
    f"{url}/rest/v1/search_results?select=*",
    headers=headers
)

if response.status_code != 200:
    print(f"Error fetching: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()
print(f"Total records: {len(data)}\n")

# Group by domain
domain_records = defaultdict(list)
for record in data:
    domain = record['domain'].lower()
    domain_records[domain].append(record)

# Find duplicates
ids_to_delete = []
for domain, records in domain_records.items():
    if len(records) > 1:
        sorted_records = sorted(records, key=lambda x: x['created_at'], reverse=True)
        for record in sorted_records[1:]:
            ids_to_delete.append(record['id'])
            print(f"Delete ID {record['id']} from {domain}")

print(f"\nTotal IDs to delete: {len(ids_to_delete)}\n")

if ids_to_delete:
    response = input("Confirm deletion? (yes/no): ").strip().lower()
    
    if response == 'yes':
        print("\n🗑️  Deleting via REST API...\n")
        
        # Delete one by one
        deleted_count = 0
        for record_id in ids_to_delete:
            resp = requests.delete(
                f"{url}/rest/v1/search_results?id=eq.{record_id}",
                headers=headers
            )
            
            if resp.status_code in [200, 204]:
                print(f"  ✓ Deleted ID: {record_id}")
                deleted_count += 1
            else:
                print(f"  ❌ Error: {resp.status_code} - {resp.text}")
        
        print(f"\n✅ Deleted {deleted_count}/{len(ids_to_delete)} records")
        
        # Verify
        print("\nFetching updated data...")
        resp = requests.get(
            f"{url}/rest/v1/search_results?select=*",
            headers=headers
        )
        data_after = resp.json()
        unique_after = len(set(r['domain'].lower() for r in data_after))
        
        print(f"\n{'='*100}")
        print("CLEANUP RESULT")
        print(f"{'='*100}")
        print(f"  Records before: 119")
        print(f"  Records deleted: {len(ids_to_delete)}")
        print(f"  Records after: {len(data_after)}")
        print(f"  Unique domains: {unique_after}")
        print(f"  Status: {'✅ CLEAN' if unique_after == len(data_after) else '❌ Still has duplicates'}")
        print(f"{'='*100}\n")
    else:
        print("Cancelled.")
else:
    print("No duplicates found!")
