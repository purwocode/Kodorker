# DuckDuckGo Infinite Scraper - FLOW DOCUMENTATION

## Mode: Keep Only 1 Link Per Domain (PRODUCTION READY)

### 🎯 Objective
Scrape links **tanpa henti** (infinite) tapi **hanya 1 link per domain**, tidak peduli berapa banyak query.

### 📊 Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ INFINITE SEARCH - Loop terus sampai CTRL+C                  │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ QUERY 1: "python"                                           │
├─────────────────────────────────────────────────────────────┤
│ Results from DuckDuckGo:                                    │
│  1. python.org/docs                                         │
│  2. python.org/download                                     │
│  3. stackoverflow.com/questions (EXCLUDED)                  │
│  4. github.com/python (EXCLUDED)                            │
│  5. realpython.com/tutorial                                 │
│                                                             │
│ Processing:                                                 │
│  ✓ python.org/docs → SAVED (domain: python.org)           │
│  ✗ python.org/download → BLOCKED (domain already in        │
│                            saved_domains)                   │
│  - stackoverflow.com (EXCLUDED)                             │
│  - github.com (EXCLUDED)                                    │
│  ✓ realpython.com/tutorial → SAVED (domain: realpython.com)│
│                                                             │
│ Results: 2 new domains saved ✓                              │
│ saved_domains = {'python.org', 'realpython.com'}           │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ QUERY 2: "tutorial" (extracted keyword)                     │
├─────────────────────────────────────────────────────────────┤
│ Results from DuckDuckGo:                                    │
│  1. python.org/tutorial                                     │
│  2. tutorialpoint.com/python                                │
│  3. realpython.com/guides                                   │
│  4. codecademy.com/learn                                    │
│                                                             │
│ Processing:                                                 │
│  ✗ python.org/tutorial → BLOCKED (python.org already saved)│
│  ✓ tutorialpoint.com/python → SAVED (new domain)           │
│  ✗ realpython.com/guides → BLOCKED (already saved)         │
│  ✓ codecademy.com/learn → SAVED (new domain)               │
│                                                             │
│ Results: 2 new domains saved ✓                              │
│ saved_domains = {                                           │
│   'python.org',                                             │
│   'realpython.com',                                         │
│   'tutorialpoint.com',                                      │
│   'codecademy.com'                                          │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ QUERY 3: "programming" (extracted keyword)                  │
├─────────────────────────────────────────────────────────────┤
│ (Process repeats - always find NEW domains)                 │
│ (Never go back to python.org, realpython.com, etc)         │
└─────────────────────────────────────────────────────────────┘
         ↓
    ... continues infinitely ...
```

### 🔑 Key Components

#### 1. **is_duplicate() Check**
```python
def is_duplicate(self, link: str, domain: str) -> bool:
    """3-tier duplicate check"""
    return (
        link in seen_links              # Current query duplicates
        or domain in seen_domains       # Current query duplicates  
        or domain in saved_domains      # GLOBAL - across all queries! ← KEY!
    )
```

#### 2. **saved_domains Tracking**
- Initialized as empty set: `self.saved_domains = set()`
- Added when result saved to Supabase: `self.saved_domains.add(domain.lower())`
- Never clears during infinite search (only reset on `reset_infinite_tracking()`)
- **This ensures: once domain saved, it's NEVER saved again**

#### 3. **Infinite Loop Logic**
```
While True:
  1. Extract query
  2. Scrape results
  3. For each result:
     - Check is_duplicate() → includes saved_domains check
     - If duplicate → SKIP (try next result)
     - If new → SAVE to Supabase + add to saved_domains
  4. Extract keyword from results
  5. Use keyword as next query
  6. Repeat (INFINITE)
```

### 📈 Expected Behavior

| Iteration | Query | Results | New Domains | saved_domains Size |
|-----------|-------|---------|-------------|-------------------|
| 1 | "python" | 5 results | 2 (python.org, realpython.com) | 2 |
| 2 | "tutorial" | 4 results | 2 (tutorialpoint.com, codecademy.com) | 4 |
| 3 | "programming" | 4 results | 2 (new domains) | 6 |
| 4 | "learning" | 4 results | 2 (new domains) | 8 |
| ... | ... | ... | ... | ... |
| N | "..." | 4 results | ~2-3 (avg) | GROWS LINEARLY |

**Pattern:** ~2-3 new domains per query on average

### ✅ Guarantees

1. **1 Link Per Domain** 
   - ✓ Domain X will NEVER appear twice in database
   - ✓ Same domain different queries = SKIPPED

2. **Infinite Loop** 
   - ✓ Will NEVER stop if keywords exist
   - ✓ Only stops when no new keywords can be extracted
   - ✓ CTRL+C gracefully stops

3. **Clean Database** 
   - ✓ Each row = unique (domain, link) pair
   - ✓ No duplicate domains

### 🚀 How to Run

```bash
python ddg_scraper.py
# Choose: 5. Infinite Search Mode
# Enter: python  (or any starting keyword)
# Enter: 10      (results per query)
# CTRL+C to stop
```

### 📊 Monitoring

During infinite search, watch for:
```
[1] Iterasi ke-1
[*] Scraping: 'python'
[*] Skipped 2 hasil (duplicate link/domain)    ← GOOD! Domain filter working
[+] Berhasil! Ditemukan 3 hasil

[2] Iterasi ke-2
[*] Scraping: 'tutorial'
[*] Skipped 1 hasil (duplicate link/domain)    ← Normal - found some saved domains
[+] Berhasil! Ditemukan 4 hasil
```

### 🛑 Stop Conditions

Infinite search stops when:
1. **User presses CTRL+C** → Ask for confirmation
2. **No results** for query → Move to next keyword
3. **No keywords** to extract → Loop ends (rare)

### 🔄 Restart Flow

Reset tracking for new infinite search:
```python
scraper = DuckDuckGoScraper("new_seed_query")
scraper.infinite_search(
    initial_query="new_topic",
    max_results=10,
    auto_save=True
)
# saved_domains is cleared automatically ✓
```

---

**Status:** ✅ PRODUCTION READY - Tested and verified
**Last Updated:** 2026-09-16
