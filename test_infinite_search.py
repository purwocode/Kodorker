#!/usr/bin/env python3
"""
Quick test: Verify "1 Link Per Domain" in Infinite Search
"""

from ddg_scraper import DuckDuckGoScraper
import time

print("\n" + "="*100)
print("TESTING: Keep Only 1 Link Per Domain - Infinite Search")
print("="*100)
print("\nTest akan:")
print("  1. Jalankan infinite search 5 iterasi")
print("  2. Track domain count per query")
print("  3. Verify TIDAK ADA domain yang muncul 2x")
print("  4. Verify saved_domains terus bertambah")
print("\n" + "="*100 + "\n")

scraper = DuckDuckGoScraper("python")

# Override untuk 5 iterasi saja
iteration = 0
max_iterations = 5
saved_domains_history = []

try:
    while iteration < max_iterations:
        iteration += 1
        
        if scraper.query.lower() in scraper.used_queries:
            keywords = scraper.extract_keywords_from_titles(limit=10)
            if not keywords:
                break
            scraper.query = keywords[0]
        
        scraper.used_queries.add(scraper.query.lower())
        
        print(f"\n[{iteration}] Query: '{scraper.query}'")
        print(f"    saved_domains (before): {len(scraper.saved_domains)}")
        
        results = scraper.scrape(max_results=10)
        
        if not results:
            print(f"    No results, stopping.")
            break
        
        print(f"    Results found: {len(results)}")
        
        # Track domains in this query
        domains_this_query = set()
        for r in results:
            domains_this_query.add(r['domain'])
        
        print(f"    Unique domains: {', '.join(sorted(domains_this_query)[:3])}...")
        
        scraper.all_results.extend(results)
        
        # Save to Supabase
        scraper.save_to_supabase()
        
        print(f"    saved_domains (after): {len(scraper.saved_domains)}")
        saved_domains_history.append(len(scraper.saved_domains))
        
        # Extract next keyword
        next_keywords = scraper.extract_keywords_from_titles(limit=10)
        if not next_keywords:
            print(f"    No keywords for next query.")
            break
        
        scraper.query = next_keywords[0]
        
        time.sleep(1)

except KeyboardInterrupt:
    print(f"\n\nStopped by user")

# Verify results
print(f"\n\n{'='*100}")
print("VERIFICATION RESULTS")
print(f"{'='*100}\n")

print(f"Total iterations: {iteration}")
print(f"Total results collected: {len(scraper.all_results)}")
print(f"Total unique domains: {len(scraper.saved_domains)}")
print(f"saved_domains growth: {saved_domains_history}\n")

# Check for duplicate domains
domain_count = {}
for result in scraper.all_results:
    domain = result['domain'].lower()
    domain_count[domain] = domain_count.get(domain, 0) + 1

duplicates = {d: c for d, c in domain_count.items() if c > 1}

if duplicates:
    print("[FAIL] Found duplicate domains in results:")
    for domain, count in duplicates.items():
        print(f"  {domain}: {count} times")
else:
    print("[PASS] NO duplicate domains found!")
    print(f"  Each domain appears exactly 1 time")
    print(f"  Total: {len(domain_count)} unique domains")

print(f"\n{'='*100}")
