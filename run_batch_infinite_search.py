#!/usr/bin/env python3
"""
Batch Infinite Search Runner - Read keywords dari list.txt
Jalankan infinite search untuk setiap keyword di list.txt
Maintain global saved_domains across all keywords (1 link per domain)
"""

from ddg_scraper import DuckDuckGoScraper
import sys
import os
from datetime import datetime

def load_keywords_from_file(filename: str) -> list:
    """Load keywords dari file (1 keyword per line)"""
    if not os.path.exists(filename):
        print(f"[-] File '{filename}' tidak ditemukan!")
        print(f"[*] Membuat file kosong...")
        with open(filename, 'w') as f:
            f.write("python\n")
            f.write("javascript\n")
            f.write("machine learning\n")
        print(f"[+] File '{filename}' dibuat. Silakan edit dan jalankan lagi.")
        return []
    
    keywords = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines dan comments
                keywords.append(line)
    
    return keywords

def main():
    print("\n" + "="*100)
    print("[BATCH INFINITE SEARCH] - Read from list.txt")
    print("="*100)
    print("\nMode: Batch processing keywords dari list.txt")
    print("      Global saved_domains: maintain across all keywords")
    print("      Guarantee: 1 link per domain (tidak peduli keyword mana)")
    print("      Dashboard: https://kodorker.vercel.app/dashboard")
    print("      Tekan CTRL+C untuk stop\n")
    
    # Get max results per query (from argument or default)
    if len(sys.argv) > 1:
        try:
            max_results = int(sys.argv[1])
        except ValueError:
            max_results = 10
    else:
        try:
            max_results = int(input("Max results per query (default 10): ") or "10")
        except ValueError:
            max_results = 10
    
    # Load keywords from file
    filename = "list.txt"
    keywords = load_keywords_from_file(filename)
    
    if not keywords:
        print("[-] Tidak ada keywords ditemukan di list.txt")
        return
    
    print(f"\n[+] Ditemukan {len(keywords)} keywords:")
    for i, kw in enumerate(keywords[:10], 1):
        print(f"    {i}. {kw}")
    if len(keywords) > 10:
        print(f"    ... dan {len(keywords) - 10} keywords lainnya")
    
    print(f"\n{'='*100}\n")
    
    # Initialize main scraper (untuk track global saved_domains)
    main_scraper = DuckDuckGoScraper(keywords[0])
    
    # Global tracking
    total_results = 0
    total_keywords_processed = 0
    
    try:
        for keyword_idx, keyword in enumerate(keywords, 1):
            print(f"\n[{keyword_idx}/{len(keywords)}] Batch: '{keyword}'")
            print(f"{'='*100}\n")
            
            # Create scraper untuk keyword ini
            scraper = DuckDuckGoScraper(keyword)
            
            # Inherit global saved_domains dari session (biar tidak duplicate across keywords)
            scraper.saved_domains = main_scraper.saved_domains.copy()
            
            # Run infinite search untuk keyword ini
            print(f"[*] Start infinite search: '{keyword}'")
            print(f"[*] Max per query: {max_results}")
            print(f"[*] Global unique domains tracked: {len(scraper.saved_domains)}\n")
            
            results = scraper.infinite_search(
                initial_query=keyword,
                max_results=max_results,
                auto_save=True  # Auto-save to Supabase
            )
            
            # Update global tracking
            main_scraper.saved_domains.update(scraper.saved_domains)
            total_results += len(results)
            total_keywords_processed += 1
            
            # Summary untuk keyword ini
            print(f"\n[*] Keyword '{keyword}' Summary:")
            print(f"    Results: {len(results)}")
            print(f"    Queries executed: {len(scraper.used_queries)}")
            print(f"    Queries: {sorted(scraper.used_queries)}")
            print(f"    Global unique domains so far: {len(main_scraper.saved_domains)}\n")
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*100}")
        print("[!] Batch infinite search dihentikan oleh user")
        print(f"{'='*100}")
    
    # Final summary
    print(f"\n\n{'='*100}")
    print("[BATCH SUMMARY] INFINITE SEARCH")
    print(f"{'='*100}\n")
    print(f"[+] Keywords diproses: {total_keywords_processed}/{len(keywords)}")
    print(f"[+] Total hasil: {total_results}")
    print(f"[+] Total unique domains (global): {len(main_scraper.saved_domains)}")
    print(f"[+] Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{'='*100}")
    print("[+] Semua data sudah tersimpan di Supabase!")
    print(f"[*] Check dashboard: https://kodorker.vercel.app/dashboard")
    print(f"{'='*100}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program dihentikan")
    except Exception as e:
        print(f"\n[-] Error: {e}")
        import traceback
        traceback.print_exc()
