#!/usr/bin/env python3
"""
Cleanup duplicate domains from Supabase
Menghapus entries duplikat sambil keep yang terbaru
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

if not url or not key:
    print('[-] .env tidak ditemukan')
    exit(1)

supabase = create_client(url, key)

print('╔════════════════════════════════════════════════════════════════╗')
print('║        SUPABASE DUPLICATE CLEANUP TOOL                         ║')
print('╚════════════════════════════════════════════════════════════════╝')
print()

# Get all results
response = supabase.table('search_results').select('*').execute()
data = response.data

print(f'[*] Total entries di database: {len(data)}')
print()

# Find duplicates by domain
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

# Find duplicates
duplicates = {d: entries for d, entries in domain_entries.items() if len(entries) > 1}

print(f'[+] Domains dengan duplikat: {len(duplicates)}')
print()

if not duplicates:
    print('[✅] Tidak ada duplikat. Database sudah clean!')
    exit(0)

print('[!] DUPLIKAT YANG AKAN DIHAPUS:')
print('=' * 70)

ids_to_delete = []
for domain, entries in duplicates.items():
    # Sort by created_at, keep yang terbaru (last one)
    sorted_entries = sorted(entries, key=lambda x: x['created_at'])
    
    print(f'\nDomain: {domain}')
    print('-' * 70)
    
    for i, entry in enumerate(sorted_entries, 1):
        created = entry['created_at'][:10]
        if i < len(sorted_entries):  # Not the latest
            print(f'  ❌ ID {entry["id"]} | Created: {created} | AKAN DIHAPUS')
            ids_to_delete.append(entry['id'])
        else:  # Latest one
            print(f'  ✅ ID {entry["id"]} | Created: {created} | KEEP (terbaru)')

print()
print('=' * 70)
print(f'[*] Total entries yang akan dihapus: {len(ids_to_delete)}')
print()

if ids_to_delete:
    confirm = input('[?] Lanjutkan delete? (yes/no): ').strip().lower()
    
    if confirm == 'yes':
        print()
        print('[*] Menghapus duplicate entries...')
        
        deleted_count = 0
        for id_to_delete in ids_to_delete:
            try:
                supabase.table('search_results').delete().eq('id', id_to_delete).execute()
                deleted_count += 1
                print(f'  ✓ Deleted ID {id_to_delete}')
            except Exception as e:
                print(f'  ✗ Error deleting ID {id_to_delete}: {e}')
        
        print()
        print(f'[✅] Berhasil menghapus {deleted_count} entries!')
        print(f'[*] Database sekarang memiliki {len(data) - deleted_count} entries unik')
    else:
        print('[*] Dibatalkan')
else:
    print('[✅] Tidak ada entries untuk dihapus')
