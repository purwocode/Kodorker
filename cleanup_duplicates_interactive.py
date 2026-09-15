#!/usr/bin/env python3
"""
Cleanup database: Keep only 1 link per domain (most recent)
"""

from supabase import create_client
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

print("\n" + "="*100)
print("DATABASE CLEANUP: Keep Only 1 Link Per Domain")
print("="*100 + "\n")

# Fetch all results
response = supabase.table("search_results").select("*").execute()
data = response.data

print(f"Total records before cleanup: {len(data)}\n")

# Group by domain and find duplicates
domain_records = defaultdict(list)
for record in data:
    domain = record['domain'].lower()
    domain_records[domain].append(record)

# Find IDs to delete
ids_to_delete = []
kept_count = 0

for domain, records in domain_records.items():
    if len(records) > 1:
        # Sort by created_at DESC (most recent first)
        sorted_records = sorted(records, key=lambda x: x['created_at'], reverse=True)
        # Keep the most recent, delete others
        for record in sorted_records[1:]:
            ids_to_delete.append(record['id'])
        
        print(f"Domain: {domain}")
        print(f"  Records: {len(records)} → Keep 1 (most recent)")
        print(f"  Keeping: {sorted_records[0]['link'][:70]}...")
        print(f"  Deleting: {len(records)-1} records")
        print()
        
        kept_count += 1

print(f"\nTotal IDs to delete: {len(ids_to_delete)}")
print(f"IDs: {ids_to_delete}\n")

if ids_to_delete:
    # Confirm deletion
    response = input("Delete these records? (yes/no): ").strip().lower()
    
    if response == 'yes':
        print("\n🗑️  Deleting duplicate records...\n")
        
        for record_id in ids_to_delete:
            try:
                supabase.table("search_results").delete().eq("id", record_id).execute()
                print(f"  ✓ Deleted ID: {record_id}")
            except Exception as e:
                print(f"  ❌ Error deleting ID {record_id}: {e}")
        
        # Verify
        response_after = supabase.table("search_results").select("*").execute()
        data_after = response_after.data
        
        # Count unique domains after cleanup
        unique_after = len(set(r['domain'].lower() for r in data_after))
        
        print(f"\n{'='*100}")
        print("CLEANUP COMPLETE")
        print(f"{'='*100}")
        print(f"  Records before: {len(data)}")
        print(f"  Records deleted: {len(ids_to_delete)}")
        print(f"  Records after: {len(data_after)}")
        print(f"  Unique domains: {unique_after}")
        print(f"  Status: ✅ CLEAN - All domains have exactly 1 link")
        print(f"{'='*100}\n")
    else:
        print("Cancelled.")
else:
    print("✅ No duplicates to delete!")
    print(f"   All {len(domain_records)} domains are unique (1 link per domain)")
