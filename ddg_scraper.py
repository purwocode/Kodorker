#!/usr/bin/env python3
"""
DuckDuckGo Scraper - NO BOT DETECTION VERSION dengan Supabase Integration
Mengambil semua link dari hasil pencarian DuckDuckGo dan menyimpan ke Supabase
"""

from ddgs import DDGS
import json
import csv
from typing import List, Dict
import time
from urllib.parse import urlparse
import re
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()


class DuckDuckGoScraper:
    """Scraper untuk DuckDuckGo - Tidak ada bot detection!"""
    
    # Default excluded domains (social media, video platforms, etc.)
    DEFAULT_EXCLUDED_DOMAINS = {
        # Social Media
        'x.com', 'twitter.com', 'facebook.com', 'instagram.com',
        'tiktok.com', 'reddit.com', 'linkedin.com', 'pinterest.com',
        'snapchat.com', 'threads.net', 'mastodon.social', 'wordpress.com',
        # Video Platforms
        'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
        'twitch.tv', 'rumble.com', 'odysee.com',
        # Music/Streaming
        'spotify.com', 'apple.com', 'music.apple.com', 'soundcloud.com',
        # Video Streaming Services
        'netflix.com', 'primevideo.com',
        # Google Services
        'play.google.com', 'ads.google.com',
        # Ads/Marketing
        'amazon.com', 'ebay.com', 'aliexpress.com',
        # E-commerce
        'shopee.co.id', 'tokopedia.com',
        # Developer/Code Hosting
        'github.com', 'gitlab.com', 'bitbucket.org', 'stackoverflow.com',
        # Search Engines & Tech Platforms
        'bing.com', 'yahoo.com', 'microsoft.com',
        # Other
        'wikipedia.org', 'wiki.fandom.com',  # Optional: uncomment jika ingin exclude
    }
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """Extract domain dari URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            # Remove 'www.' if present
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return url
    
    @staticmethod
    def remove_date_from_body(body: str) -> str:
        """Remove date prefix dari body (e.g., 'January 10, 2026 - ')"""
        # Pattern: Month Day(s), Year - atau short format Month Day, Year atau Month Year -
        pattern = r'^[A-Za-z]+\s+\d{1,2},?\s+\d{4}\s*[–-]\s*'
        # Also handle formats like "1 month ago -" atau "Nov 6, 2023 ·"
        pattern2 = r'^(\d+\s+\w+\s+ago|Sep\s+\d+,?\s+\d{4})\s*[–·-]\s*'
        body = re.sub(pattern, '', body)
        body = re.sub(pattern2, '', body)
        return body.strip()
    
    @staticmethod
    def init_supabase():
        """Initialize Supabase connection"""
        try:
            from supabase import create_client, Client
            
            url = os.getenv('SUPABASE_URL')
            key = os.getenv('SUPABASE_KEY')
            
            if not url or not key:
                print("[-] Error: SUPABASE_URL dan SUPABASE_KEY tidak ditemukan di .env")
                print("[*] Silakan copy .env.example ke .env dan isi credentials Supabase")
                return None
            
            client: Client = create_client(url, key)
            print(f"[+] Berhasil connect ke Supabase!")
            return client
        except Exception as e:
            print(f"[-] Error connecting to Supabase: {e}")
            return None
    
    def __init__(self, query: str, max_results: int = None, delay: float = 0.5, excluded_domains: set = None):
        self.query = query
        self.max_results = max_results
        self.delay = delay
        self.results = []
        self.ddgs = DDGS()
        self.supabase = self.init_supabase()
        
        # Set excluded domains
        if excluded_domains is None:
            self.excluded_domains = self.DEFAULT_EXCLUDED_DOMAINS.copy()
        else:
            self.excluded_domains = excluded_domains
        
        # Track seen links and domains to prevent duplicates
        self.seen_links = set()
        self.seen_domains = set()
        
        # Track used queries untuk infinite search
        self.used_queries = set()
        self.all_results = []  # Simpan semua results dari semua queries
    
    def add_excluded_domain(self, domain: str):
        """Tambah domain ke excluded list"""
        self.excluded_domains.add(domain.lower())
    
    def add_excluded_domains(self, domains: list):
        """Tambah multiple domains ke excluded list"""
        for domain in domains:
            self.excluded_domains.add(domain.lower())
    
    def is_domain_excluded(self, domain: str) -> bool:
        """
        Check jika domain ada di excluded list (termasuk subdomain)
        
        Examples:
        - excluded: 'wordpress.com' 
          will also exclude: 'blogs.wordpress.com', 'my.site.wordpress.com', etc
        - excluded: 'facebook.com'
          will also exclude: 'graph.facebook.com', 'api.facebook.com', etc
        """
        domain = domain.lower()
        
        for excluded in self.excluded_domains:
            excluded_lower = excluded.lower()
            
            # Exact match (e.g., 'wordpress.com' == 'wordpress.com')
            if domain == excluded_lower:
                return True
            
            # Subdomain match (e.g., 'blogs.wordpress.com' endswith '.wordpress.com')
            if domain.endswith('.' + excluded_lower):
                return True
        
        return False
    
    def is_duplicate(self, link: str, domain: str) -> bool:
        """Check jika link atau domain sudah ada (duplicate)"""
        link_lower = link.lower()
        domain_lower = domain.lower()
        return link_lower in self.seen_links or domain_lower in self.seen_domains
    
    def add_to_tracking(self, link: str, domain: str):
        """Tambah link dan domain ke tracking set"""
        self.seen_links.add(link.lower())
        self.seen_domains.add(domain.lower())
    
    def clear_duplicates(self):
        """Clear duplicate tracking untuk scrape baru"""
        self.seen_links.clear()
        self.seen_domains.clear()
        print("[*] Duplicate tracking cleared")
    
    
    def extract_keywords_from_titles(self, limit: int = 20) -> List[str]:
        """Ekstrak keywords per-kata dari titles hasil scraping"""
        if not self.results:
            return []
        
        keywords = []
        common_words = {'the', 'a', 'an', 'is', 'are', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'how', 'what', 'when', 'where', 'why', 'about', 'facts', 'guide', 'tutorial', 'learn', '–', '-', '|', ',', '.', '(', ')'}
        
        # Extract kata per kata dari semua results
        for result in self.results[:limit]:
            title = result.get('title', '')
            words = title.lower().split()
            
            for word in words:
                # Clean punctuation
                word = re.sub(r'[^\w]', '', word)
                
                # Filter: meaningful words only
                if (word and len(word) > 2 and 
                    word not in common_words and 
                    word.lower() not in [k.lower() for k in keywords] and
                    word.lower() not in self.used_queries):
                    keywords.append(word)
                    
                    if len(keywords) >= limit:
                        return keywords
        
        return keywords[:limit]
    
    def reset_infinite_tracking(self):
        """Reset tracking untuk infinite search baru"""
        self.used_queries.clear()
        self.all_results = []
        print("[*] Infinite search tracking reset")
    
    def scrape(self, max_results: int = 20, retries: int = 3) -> List[Dict]:
        """
        Scrape DuckDuckGo search results dengan retry logic
        
        Args:
            max_results: Jumlah hasil maksimal yang ingin diambil
            retries: Jumlah retry jika ada network error
            
        Returns:
            List of search results dengan structure:
            {
                'title': str,
                'body': str (description/snippet),
                'domain': str (extracted domain),
                'link': str (full URL)
            }
        """
        for attempt in range(1, retries + 1):
            try:
                print(f"[*] Scraping DuckDuckGo untuk: '{self.query}'")
                print(f"[*] Max results: {max_results}")
                
                raw_results = list(self.ddgs.text(
                    self.query,
                    max_results=max_results,
                    timelimit='y'  # Hasil 1 tahun terakhir
                ))
                
                # Transform to title + body + domain + link format
                self.results = []
                self.clear_duplicates()  # Reset tracking untuk scrape baru
                skipped_excluded = 0
                skipped_duplicate = 0
                
                for result in raw_results:
                    title = result.get('title', '')
                    body = self.remove_date_from_body(result.get('body', ''))
                    href = result.get('href', '')
                    domain = self.extract_domain(href)
                    
                    # Skip jika domain ada di excluded list
                    if self.is_domain_excluded(domain):
                        skipped_excluded += 1
                        continue
                    
                    # Skip jika link atau domain sudah ada (duplicate)
                    if self.is_duplicate(href, domain):
                        skipped_duplicate += 1
                        continue
                    
                    transformed = {
                        'title': title,
                        'body': body,
                        'domain': domain,
                        'link': href
                    }
                    self.results.append(transformed)
                    self.add_to_tracking(href, domain)  # Track hasil yang diambil
                
                if skipped_excluded > 0:
                    print(f"[*] Skipped {skipped_excluded} hasil dari excluded domains")
                if skipped_duplicate > 0:
                    print(f"[*] Skipped {skipped_duplicate} hasil (duplicate link/domain)")
                
                print(f"[+] Berhasil! Ditemukan {len(self.results)} hasil\n")
                
                return self.results
                
            except Exception as e:
                error_msg = str(e)
                
                # Check if it's a network error (connection refused, timeout, etc)
                is_network_error = any(err in error_msg.lower() for err in [
                    'connection refused', 'connection timeout', 'connection reset',
                    'timeouterror', 'connectionerror', 'os error 111', 'os error 110'
                ])
                
                if is_network_error and attempt < retries:
                    # Network error - retry setelah delay
                    wait_time = 5 * attempt  # 5s, 10s, 15s exponential backoff
                    print(f"[!] Network error (attempt {attempt}/{retries}): {e}")
                    print(f"[*] Retrying dalam {wait_time} detik...")
                    time.sleep(wait_time)
                    continue
                else:
                    # Either not network error, atau sudah max retries
                    if is_network_error:
                        print(f"[-] Network error after {retries} retries: {e}")
                        print(f"[-] Skipping query '{self.query}' (network issue)")
                    else:
                        print(f"[-] Error: {e}")
                    return []
        
        return []
    
    def print_results(self, limit: int = None):
        """Tampilkan hasil ke console"""
        
        results_to_show = self.results[:limit] if limit else self.results
        
        print("="*100)
        print(f"Hasil Pencarian: {self.query}")
        print(f"Total: {len(self.results)} hasil")
        print("="*100 + "\n")
        
        for i, result in enumerate(results_to_show, 1):
            print(f"{i}. Domain: {result['domain']}")
            print(f"   Title: {result['title']}")
            print(f"   Body: {result['body'][:80]}..." if len(result['body']) > 80 else f"   Body: {result['body']}")
            print(f"   Link: {result['link']}")
            print()
    
    def infinite_search(self, initial_query: str, max_results: int = 10, auto_save: bool = False):
        """Infinite search - scrape lalu gunakan extracted keywords (per-kata) sebagai query baru
        
        Args:
            initial_query: Query awal
            max_results: Hasil per query
            auto_save: Otomatis save ke Supabase setiap query
        """
        self.query = initial_query
        self.reset_infinite_tracking()
        iteration = 0
        
        print(f"\n{'='*100}")
        print(f"INFINITE SEARCH MODE - Tekan CTRL+C untuk berhenti")
        print(f"Keyword extraction: Per-word dari title (cepat)")
        print(f"{'='*100}\n")
        
        try:
            while True:
                iteration += 1
                
                # Cek jika query sudah pernah digunakan
                if self.query.lower() in self.used_queries:
                    print(f"[!] Query '{self.query}' sudah digunakan sebelumnya, mencari keyword alternatif...")
                    keywords = self.extract_keywords_from_titles(limit=10)
                    
                    if not keywords:
                        print(f"[!] Tidak ada keyword baru yang tersedia. Infinite search selesai.")
                        break
                    
                    self.query = keywords[0]
                    print(f"[*] Menggunakan query baru: '{self.query}'")
                
                self.used_queries.add(self.query.lower())
                
                # Scrape dengan query saat ini
                print(f"\n[{iteration}] Iterasi ke-{iteration}")
                print(f"[*] Scraping: '{self.query}'")
                
                results = self.scrape(max_results=max_results)
                
                if not results:
                    print(f"[!] Tidak ada hasil untuk query '{self.query}', scrape selesai.")
                    break
                
                # Simpan ke all_results
                self.all_results.extend(results)
                
                # Optional: auto save ke Supabase
                if auto_save:
                    self.save_to_supabase()
                
                # Extract keywords untuk query berikutnya
                next_keywords = self.extract_keywords_from_titles(limit=10)
                
                if not next_keywords:
                    print(f"[!] Tidak ada keyword untuk lanjut scraping.")
                    break
                
                # Gunakan keyword pertama sebagai query berikutnya
                self.query = next_keywords[0]
                print(f"[*] Keyword berikutnya: '{self.query}'")
                
                # Delay untuk tidak overload server
                time.sleep(self.delay)
        
        except KeyboardInterrupt:
            print(f"\n\n{'='*100}")
            response = input("[?] Are you sure to stop this program? (y/Enter): ").strip().lower()
            if response == 'y' or response == '':
                print(f"[+] Program dihentikan.")
                print(f"[*] Total scraping iterations: {iteration}")
                print(f"[*] Total hasil dikumpulkan: {len(self.all_results)}")
                print(f"[*] Total queries unik: {len(self.used_queries)}")
                print(f"{'='*100}\n")
                return self.all_results
            else:
                print(f"[*] Lanjut scraping...\n")
                return self.infinite_search(self.query, max_results, auto_save)
        
        # Return results ketika loop break (normal completion)
        return self.all_results
    
    def get_infinite_results(self):
        """Get semua results dari infinite search"""
        return self.all_results
    
    def save_infinite_results(self, filename: str = 'infinite_results.json'):
        """Simpan semua results dari infinite search ke file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'total_results': len(self.all_results),
                    'total_queries': len(self.used_queries),
                    'queries_used': list(self.used_queries),
                    'results': self.all_results
                }, f, ensure_ascii=False, indent=2)
            print(f"[+] Semua hasil disimpan ke: {filename}")
            return True
        except Exception as e:
            print(f"[-] Error: {e}")
            return False
    
    def save_json(self, filename: str = 'ddg_results.json'):
        """Simpan hasil ke JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"[+] Hasil disimpan ke: {filename}")
        except Exception as e:
            print(f"[-] Error: {e}")
    
    def save_csv(self, filename: str = 'ddg_results.csv'):
        """Simpan hasil ke CSV"""
        try:
            if not self.results:
                print("[-] Tidak ada hasil untuk disimpan")
                return
            
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['domain', 'title', 'body', 'link'])
                writer.writeheader()
                writer.writerows(self.results)
            
            print(f"[+] Hasil disimpan ke: {filename}")
        except Exception as e:
            print(f"[-] Error: {e}")
    
    def save_txt(self, filename: str = 'ddg_results.txt'):
        """Simpan hasil ke TXT"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Hasil Pencarian DuckDuckGo: {self.query}\n")
                f.write("="*100 + "\n")
                f.write(f"Total hasil: {len(self.results)}\n")
                f.write("="*100 + "\n\n")
                
                for i, result in enumerate(self.results, 1):
                    f.write(f"{i}.\n")
                    f.write(f"Domain: {result['domain']}\n")
                    f.write(f"Title: {result['title']}\n")
                    f.write(f"Body: {result['body']}\n")
                    f.write(f"Link: {result['link']}\n")
                    f.write("\n")
            
            print(f"[+] Hasil disimpan ke: {filename}")
        except Exception as e:
            print(f"[-] Error: {e}")
    
    def save_to_supabase(self, table_name: str = 'search_results') -> bool:
        """Simpan hasil ke Supabase (bisa semua atau hanya current results)"""
        if not self.supabase:
            print("[-] Supabase tidak terhubung")
            return False
        
        results_to_save = self.results if self.results else self.all_results
        
        if not results_to_save:
            print("[-] Tidak ada hasil untuk disimpan")
            return False
        
        try:
            print(f"[*] Menyimpan {len(results_to_save)} hasil ke Supabase...")
            
            # Prepare data with query information
            data_to_insert = []
            for result in results_to_save:
                data_to_insert.append({
                    'query': result.get('query', self.query),
                    'title': result['title'],
                    'body': result['body'],
                    'domain': result['domain'],
                    'link': result['link']
                })
            
            # Insert data to Supabase
            response = self.supabase.table(table_name).insert(data_to_insert).execute()
            
            print(f"[+] Berhasil! {len(results_to_save)} hasil disimpan ke Supabase (tabel: {table_name})")
            return True
            
        except Exception as e:
            error_msg = str(e)
            # Handle duplicate key constraint error
            if '23505' in error_msg or 'duplicate key' in error_msg.lower():
                print(f"[!] Beberapa hasil sudah ada di Supabase (duplicate links), coba save dengan filter...")
                # Try saving without duplicates if possible
                try:
                    successful_count = 0
                    failed_count = 0
                    for item in data_to_insert:
                        try:
                            self.supabase.table(table_name).insert([item]).execute()
                            successful_count += 1
                        except Exception as item_error:
                            if '23505' in str(item_error) or 'duplicate key' in str(item_error).lower():
                                failed_count += 1
                            else:
                                raise
                    
                    print(f"[+] Berhasil! {successful_count} hasil disimpan (duplikat: {failed_count} skipped)")
                    return True
                except Exception as inner_error:
                    print(f"[-] Gagal save individual items: {inner_error}")
                    return False
            else:
                print(f"[-] Error saving to Supabase: {e}")
                return False


def example_basic():
    """Contoh: Basic scraping"""
    print("\n" + "="*100)
    print("CONTOH 1: Basic Scraping")
    print("="*100 + "\n")
    
    scraper = DuckDuckGoScraper("Python Programming")
    scraper.scrape(max_results=10)
    scraper.print_results(limit=5)
    scraper.save_json('example1_python.json')


def example_multiple_keywords():
    """Contoh: Multiple keywords"""
    print("\n" + "="*100)
    print("CONTOH 2: Multiple Keywords")
    print("="*100 + "\n")
    
    keywords = ["Machine Learning", "Web Development", "Data Science"]
    
    for keyword in keywords:
        print(f"\n[*] Scraping: {keyword}")
        scraper = DuckDuckGoScraper(keyword)
        scraper.scrape(max_results=5)
        scraper.save_json(f'ddg_{keyword.replace(" ", "_").lower()}.json')
        print(f"[+] Done! Disimpan ke: ddg_{keyword.replace(' ', '_').lower()}.json")
        time.sleep(1)  # Delay antar keyword


def example_filter_results():
    """Contoh: Filter hasil"""
    print("\n" + "="*100)
    print("CONTOH 3: Filter Hasil")
    print("="*100 + "\n")
    
    scraper = DuckDuckGoScraper("GitHub Repositories")
    scraper.scrape(max_results=15)
    
    print(f"[*] Total hasil: {len(scraper.results)}")
    
    # Filter: hanya GitHub
    github_results = [r for r in scraper.results if 'github.com' in r['domain']]
    print(f"[*] Hasil dari GitHub: {len(github_results)}\n")
    
    for i, result in enumerate(github_results[:5], 1):
        print(f"{i}. Domain: {result['domain']}")
        print(f"   Title: {result['title']}")
        print(f"   {result['link']}\n")


def example_all_formats():
    """Contoh: Simpan semua format + Supabase"""
    print("\n" + "="*100)
    print("CONTOH 4: Simpan Semua Format + Supabase")
    print("="*100 + "\n")
    
    scraper = DuckDuckGoScraper("Web API Design")
    scraper.scrape(max_results=20)
    
    scraper.print_results(limit=5)
    
    # Save to Supabase (primary)
    scraper.save_to_supabase(table_name='search_results')
    
    print("\n[+] Semua data disimpan ke Supabase!")


def example_infinite_search():
    """Contoh: Infinite Search Mode - Auto extract keywords & continue searching"""
    print("\n" + "="*100)
    print("CONTOH 5: Infinite Search Mode")
    print("="*100)
    print("Fitur ini akan:")
    print("  1. Mulai dari query awal")
    print("  2. Ekstrak keywords dari hasil")
    print("  3. Gunakan keywords sebagai query berikutnya")
    print("  4. Lanjut terus sampai CTRL+C")
    print("  5. Tekan CTRL+C untuk confirm stop\n")
    
    scraper = DuckDuckGoScraper("Artificial Intelligence")
    
    # Start infinite search
    # max_results=5 untuk testing, bisa dinaikkan
    # auto_save=True akan otomatis save ke Supabase setiap query
    results = scraper.infinite_search(
        initial_query="Artificial Intelligence",
        max_results=5,
        auto_save=True
    )
    
    # Summary
    print(f"\n[+] Infinite search selesai!")
    print(f"[*] Total hasil: {len(results)}")
    print(f"[*] Total queries: {len(scraper.used_queries)}")
    print(f"[*] Queries: {scraper.used_queries}\n")
    
    # Save all results to JSON
    scraper.save_infinite_results('infinite_results.json')
    
    # Optional: display some results
    if results:
        print(f"\n[*] Sample hasil (5 pertama):")
        for i, result in enumerate(results[:5], 1):
            print(f"{i}. {result['domain']}: {result['title'][:60]}...")


def example_test_subdomain_exclusion():
    """Contoh: Test subdomain exclusion"""
    print("\n" + "="*100)
    print("CONTOH: Test Subdomain Exclusion")
    print("="*100 + "\n")
    
    scraper = DuckDuckGoScraper("Test Query")
    
    # Test domains yang seharusnya di-exclude
    test_cases = [
        # (domain_to_test, should_be_excluded, reason)
        ("wordpress.com", True, "Exact match"),
        ("blogs.wordpress.com", True, "Subdomain of wordpress.com"),
        ("mysite.blogs.wordpress.com", True, "Sub-subdomain of wordpress.com"),
        ("wordpress.co", False, "Different domain (not wordpress.com)"),
        ("wordpress.com.fake", False, "Fake domain (com.fake suffix)"),
        ("twitter.com", True, "Exact match"),
        ("api.twitter.com", True, "Subdomain of twitter.com"),
        ("x.com", True, "Exact match (X/Twitter)"),
        ("my.site.x.com", True, "Sub-subdomain of x.com"),
        ("github.com", False, "Not in excluded list"),
        ("www.github.com", False, "Not in excluded list"),
        ("wikipedia.org", True, "Exact match"),
        ("en.wikipedia.org", True, "Subdomain of wikipedia.org"),
        ("fr.wikipedia.org", True, "Subdomain of wikipedia.org"),
        ("facebook.com", True, "Exact match"),
        ("graph.facebook.com", True, "Subdomain of facebook.com"),
        ("api.facebook.com", True, "Subdomain of facebook.com"),
    ]
    
    print("[*] Testing subdomain exclusion logic...\n")
    
    passed = 0
    failed = 0
    
    for domain, should_exclude, reason in test_cases:
        is_excluded = scraper.is_domain_excluded(domain)
        status = "✓" if is_excluded == should_exclude else "✗"
        
        if is_excluded == should_exclude:
            passed += 1
            result = "PASS"
        else:
            failed += 1
            result = "FAIL"
        
        print(f"{status} [{result}] {domain:<40} Expected: {str(should_exclude):<6} Got: {str(is_excluded):<6} ({reason})")
    
    print(f"\n{'='*100}")
    print(f"[+] Results: {passed} passed, {failed} failed")
    print(f"{'='*100}\n")
    
    if failed == 0:
        print("✅ Semua subdomain exclusion tests passed!\n")
    else:
        print("❌ Ada beberapa test yang gagal. Cek konfigurasi excluded_domains\n")


def example_infinite_search_with_input(initial_query: str, max_results: int = None):
    """Infinite Search dengan input query dan max_results dari user"""
    # Jika max_results tidak diberikan, minta input dari user
    if max_results is None:
        while True:
            try:
                max_results_input = input("[?] Berapa hasil per query? (default 10): ").strip()
                max_results = int(max_results_input) if max_results_input else 10
                if max_results <= 0:
                    print("[!] Nilai harus > 0")
                    continue
                break
            except ValueError:
                print("[!] Input tidak valid, gunakan angka")
    
    scraper = DuckDuckGoScraper(initial_query)
    
    print("\n" + "="*100)
    print(f"INFINITE SEARCH MODE - Query Awal: '{initial_query}' | Max Results: {max_results}")
    print("="*100)
    print("Fitur ini akan:")
    print("  1. Mulai dari query Anda")
    print("  2. Ekstrak keywords per-kata dari hasil (cepat)")
    print("  3. Gunakan keywords sebagai query berikutnya")
    print("  4. Lanjut terus sampai CTRL+C")
    print("  5. Tekan CTRL+C untuk confirm stop\n")
    
    results = scraper.infinite_search(
        initial_query=initial_query,
        max_results=max_results,
        auto_save=True
    )
    
    # Handle None case (shouldn't happen now but defensive)
    if results is None:
        results = scraper.all_results
    
    # Summary
    print(f"\n[+] Infinite search selesai!")
    print(f"[*] Total hasil: {len(results)}")
    print(f"[*] Total queries: {len(scraper.used_queries)}")
    print(f"[*] Queries: {scraper.used_queries}\n")
    
    # Save all results
    scraper.save_infinite_results('results.json')
    print(f"[+] Hasil disimpan ke: results.json")
    
    # Optional: display some results
    if results:
        print(f"\n[*] Sample hasil (5 pertama):")
        for i, result in enumerate(results[:5], 1):
            print(f"{i}. {result['domain']}: {result['title'][:60]}...")


def example_basic_with_input(query: str):
    """Basic scraping dengan input query"""
    print(f"\n[*] Scraping: '{query}'\n")
    
    scraper = DuckDuckGoScraper(query)
    scraper.scrape(max_results=20)
    scraper.print_results(limit=5)
    scraper.save_json('results.json')
    scraper.save_to_supabase()
    print(f"[+] Hasil disimpan!")


def example_multiple_keywords_with_input(keywords: list):
    """Multiple keywords scraping"""
    for keyword in keywords:
        print(f"\n[*] Scraping: {keyword}")
        scraper = DuckDuckGoScraper(keyword)
        scraper.scrape(max_results=5)
        scraper.save_json(f'results_{keyword.replace(" ", "_").lower()}.json')
        scraper.save_to_supabase()
        print(f"[+] Done! Disimpan ke: results_{keyword.replace(' ', '_').lower()}.json")
        time.sleep(1)


def example_filter_results_with_input(query: str):
    """Filter hasil scraping"""
    print(f"\n[*] Scraping: {query}\n")
    
    scraper = DuckDuckGoScraper(query)
    scraper.scrape(max_results=15)
    
    print(f"[*] Total hasil: {len(scraper.results)}")
    scraper.print_results(limit=5)
    scraper.save_to_supabase()


def example_all_formats_with_input(query: str):
    """Simpan semua format"""
    print(f"\n[*] Scraping: {query}\n")
    
    scraper = DuckDuckGoScraper(query)
    scraper.scrape(max_results=20)
    
    scraper.print_results(limit=5)
    
    # Save semua format
    scraper.save_json('results.json')
    scraper.save_csv('results.csv')
    scraper.save_txt('results.txt')
    scraper.save_to_supabase()
    
    print(f"\n[+] Hasil disimpan ke: results.json, results.csv, results.txt, Supabase")



def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║      DuckDuckGo Scraper - NO BOT DETECTION!                  ║
    ║      Dengan Supabase Integration                             ║
    ║      Scrape DuckDuckGo tanpa khawatir di-block               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("✅ Fitur:")
    print("  - Tidak ada bot detection")
    print("  - Tidak perlu proxy")
    print("  - Unlimited requests")
    print("  - Gratis (no API key needed)")
    print("  - Integrasi dengan Supabase ✨ NEW!")
    print("  - Export ke JSON, CSV, TXT")
    print("  - Infinite Search Mode ✨ NEW!")
    print("  - Automatic Subdomain Exclusion ✨ NEW!")
    
    # Menu untuk memilih mode
    print("\n" + "="*100)
    print("PILIH MODE SCRAPING:")
    print("="*100)
    print("1. Basic Scraping")
    print("2. Multiple Keywords")
    print("3. Filter Results")
    print("4. All Formats + Supabase")
    print("5. Infinite Search Mode")
    print("6. Test Subdomain Exclusion")
    print("="*100 + "\n")
    
    choice = input("Masukkan pilihan (1-6): ").strip()
    
    if choice == "1":
        query = input("\nMasukkan query: ").strip()
        if not query:
            print("[-] Query tidak boleh kosong!")
            return
        example_basic_with_input(query)
    
    elif choice == "2":
        print("\nMasukkan keywords (pisahkan dengan koma):")
        keywords_input = input("Contoh: Machine Learning, Web Development, Data Science\n> ").strip()
        if not keywords_input:
            print("[-] Keywords tidak boleh kosong!")
            return
        keywords = [k.strip() for k in keywords_input.split(",")]
        example_multiple_keywords_with_input(keywords)
    
    elif choice == "3":
        query = input("\nMasukkan query: ").strip()
        if not query:
            print("[-] Query tidak boleh kosong!")
            return
        example_filter_results_with_input(query)
    
    elif choice == "4":
        query = input("\nMasukkan query: ").strip()
        if not query:
            print("[-] Query tidak boleh kosong!")
            return
        example_all_formats_with_input(query)
    
    elif choice == "5":
        query = input("\nMasukkan query awal untuk Infinite Search: ").strip()
        if not query:
            print("[-] Query tidak boleh kosong!")
            return
        # Input max_results, jika tidak diberikan akan minta input di function
        example_infinite_search_with_input(query)
    
    elif choice == "6":
        example_test_subdomain_exclusion()
    
    else:
        print("[-] Pilihan tidak valid!")
        return
    
    print("\n" + "="*100)
    print("✅ Done!")
    print("="*100)


if __name__ == '__main__':
    main()
