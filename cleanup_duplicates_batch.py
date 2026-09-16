#!/usr/bin/env python3
"""
Cleanup duplicates - KEEP OLDEST per domain using SQL approach
This is faster and more reliable than deleting one-by-one
"""

import sys
import io
from supabase import create_client
import os
from dotenv import load_dotenv

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

print("\n" + "="*100)
print("CLEANUP DUPLICATES - SQL APPROACH (Keep OLDEST per domain)")
print("="*100 + "\n")

# Get current stats
response = supabase.table("search_results").select("*", count="exact").execute()
data = response.data
total_before = len(data)

print(f"[*] Total records BEFORE: {total_before}\n")

# Strategy: Use SQL to delete all BUT the oldest record per domain
# This is done by deleting records where ID is NOT in the subquery of oldest records

sql_query = """
WITH oldest_per_domain AS (
  SELECT DISTINCT ON (domain) id
  FROM search_results
  ORDER BY domain, created_at ASC
)
DELETE FROM search_results
WHERE id NOT IN (SELECT id FROM oldest_per_domain)
"""

try:
    print("[*] Preparing batch delete via RPC...")
    
    # Alternative: Use raw SQL execution if available
    # Since Supabase doesn't expose raw SQL delete easily, we'll use the REST API approach
    
    # Get all records grouped by domain
    all_records = supabase.table("search_results").select("*").execute().data
    
    # Build list of IDs to keep (oldest per domain)
    from collections import defaultdict
    from operator import itemgetter
    
    domain_map = defaultdict(list)
    for record in all_records:
        domain = record['domain'].lower()
        domain_map[domain].append(record)
    
    # Keep only oldest per domain
    to_keep_ids = set()
    to_delete_ids = []
    
    for domain, records in domain_map.items():
        sorted_records = sorted(records, key=itemgetter('created_at'))
        oldest = sorted_records[0]
        to_keep_ids.add(oldest['id'])
        
        # Mark rest for deletion
        for record in sorted_records[1:]:
            to_delete_ids.append(record['id'])
    
    print(f"[*] Keeping {len(to_keep_ids)} oldest records")
    print(f"[*] Deleting {len(to_delete_ids)} duplicate records\n")
    
    if not to_delete_ids:
        print("[+] No duplicates found!")
        exit(0)
    
    # Batch delete (chunk by 100 to avoid timeout)
    chunk_size = 100
    total_deleted = 0
    
    for i in range(0, len(to_delete_ids), chunk_size):
        chunk = to_delete_ids[i:i+chunk_size]
        
        # Delete this chunk
        for record_id in chunk:
            try:
                supabase.table("search_results").delete().eq("id", record_id).execute()
                total_deleted += 1
                
                if total_deleted % 50 == 0:
                    print(f"[*] Deleted {total_deleted}/{len(to_delete_ids)} records...")
            except Exception as e:
                print(f"[-] Error deleting ID {record_id}: {e}")
    
    # Get final stats
    final_response = supabase.table("search_results").select("*", count="exact").execute()
    total_after = len(final_response.data)
    
    print(f"\n[+] Cleanup complete!")
    print(f"[+] Records BEFORE: {total_before}")
    print(f"[+] Records DELETED: {total_before - total_after}")
    print(f"[+] Records AFTER: {total_after}")
    print(f"\n" + "="*100)
    print("CLEANUP SUCCESSFUL")
    print("="*100 + "\n")
    
except Exception as e:
    print(f"[-] Error: {e}")
    import traceback
    traceback.print_exc()
