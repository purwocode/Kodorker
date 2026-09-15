#!/usr/bin/env python3
"""
Infinite Search Runner - Tanpa JSON Save
Jalankan infinite search yang langsung save ke Supabase real-time
Tidak ada file JSON - hanya save to database
"""

from ddg_scraper import DuckDuckGoScraper
import sys

def main():
    print("\n" + "="*100)
    print("[INFINITE SEARCH MODE] - Real-time Supabase (No JSON)")
    print("="*100)
    print("\nMode: Auto-save to Supabase setiap query")
    print("      Tanpa JSON file - hanya database")
    print("      Dashboard: https://kodorker.vercel.app/dashboard")
    print("      Tekan CTRL+C untuk stop\n")
    
    # Get initial query and max_results from arguments
    if len(sys.argv) > 1:
        initial_query = sys.argv[1]
        max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    else:
        # Interactive mode
        initial_query = input("Masukkan query awal: ").strip()
        
        if not initial_query:
            print("[-] Query tidak boleh kosong!")
            return
        
        # Get max results per query
        try:
            max_results = int(input("Max results per query (default 10): ") or "10")
        except ValueError:
            max_results = 10
    
    print(f"\n[+] Mulai infinite search:")
    print(f"    Query: '{initial_query}'")
    print(f"    Max per query: {max_results}")
    print(f"    Auto-save: True (real-time ke Supabase)")
    print(f"\n{'='*100}\n")
    
    # Initialize scraper
    scraper = DuckDuckGoScraper(initial_query)
    
    # Run infinite search dengan auto_save=True (langsung save ke Supabase)
    results = scraper.infinite_search(
        initial_query=initial_query,
        max_results=max_results,
        auto_save=True  # ← PENTING: Auto-save to Supabase every query
    )
    
    # Summary (tanpa JSON save)
    print(f"\n\n{'='*100}")
    print("[SUMMARY] INFINITE SEARCH")
    print(f"{'='*100}\n")
    print(f"[+] Total Hasil: {len(results)}")
    print(f"[+] Total Queries: {len(scraper.used_queries)}")
    print(f"[+] Total Domains Unik: {len(scraper.saved_domains)}")
    print(f"\n[*] Queries yang digunakan:")
    for i, query in enumerate(sorted(scraper.used_queries), 1):
        print(f"    {i}. {query}")
    
    print(f"\n{'='*100}")
    print("[+] Semua data sudah tersimpan di Supabase!")
    print(f"[*] Check dashboard: https://kodorker.vercel.app/dashboard")
    print(f"{'='*100}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Infinite search dihentikan oleh user")
    except Exception as e:
        print(f"\n[-] Error: {e}")
        import traceback
        traceback.print_exc()
