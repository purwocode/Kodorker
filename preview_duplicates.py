#!/usr/bin/env python3
"""Preview duplicates tanpa delete"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

supabase = create_client(url, key)

print('╔════════════════════════════════════════════════════════════════╗')
print('║        DUPLICATE PREVIEW (No delete)                           ║')
print('╚════════════════════════════════════════════════════════════════╝')
print()

response = supabase.table('search_results').select('*').execute()
data = response.data

print(f'[+] Total entries: {len(data)}')
print()

# Find duplicates
domain_entries = {}
for r in data:
    domain = r['domain']
    if domain not in domain_entries:
        domain_entries[domain] = []
    domain_entries[domain].append({
        'id': r['id'],
        'domain': r['domain'],
        'link': r['link'],
        'created_at': r['created_at'],
    })

duplicates = {d: entries for d, entries in domain_entries.items() if len(entries) > 1}

print(f'[*] Domains dengan duplikat: {len(duplicates)}')
print()

if not duplicates:
    print('[✅] Tidak ada duplikat!')
else:
    print('[!] ENTRIES YANG BISA DIHAPUS:')
    print('=' * 70)
    
    total_delete = 0
    for domain, entries in duplicates.items():
        sorted_entries = sorted(entries, key=lambda x: x['created_at'])
        
        print(f'\nDomain: {domain} ({len(entries)} entries)')
        print('-' * 70)
        
        for i, entry in enumerate(sorted_entries, 1):
            created = entry['created_at'][:10]
            if i < len(sorted_entries):
                print(f'  ❌ ID {entry["id"]} | {created} | HAPUS (older)')
                total_delete += 1
            else:
                print(f'  ✅ ID {entry["id"]} | {created} | KEEP  (newest)')

    print()
    print('=' * 70)
    print(f'[*] Total entries yang bisa dihapus: {total_delete}')
    print(f'[*] Entries yang akan di-keep: {len(data) - total_delete}')
