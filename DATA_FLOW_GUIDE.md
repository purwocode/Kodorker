# DATA FLOW & DUPLICATE MANAGEMENT

## ❓ PERTANYAAN 1: Bagaimana cara menghapus duplikat?

### Opsi A: Menggunakan Script (RECOMMENDED)

1. **Preview duplikat (tanpa delete):**
   ```bash
   python preview_duplicates.py
   ```
   Output akan menunjukkan entries mana yang bisa dihapus.

2. **Delete duplikat (dengan konfirmasi):**
   ```bash
   python cleanup_duplicates.py
   ```
   Script akan:
   - Menampilkan entries yang akan dihapus
   - Minta konfirmasi: "yes" untuk proceed
   - Keep entry yang paling baru (terbaru)
   - Hapus entry yang lebih lama

3. **Verifikasi setelah delete:**
   ```bash
   python preview_duplicates.py
   ```
   Harus menampilkan "Tidak ada duplikat!" jika sukses.

---

### Opsi B: Delete Manual dari Supabase Dashboard

1. Buka: https://app.supabase.com → Pilih project
2. Navigate ke "Table Editor" → `search_results`
3. Lihat entries dengan domain yang sama
4. Delete manual yang lebih lama (keep yang terbaru)

**Constraint:** `link` field harus unique, jadi tidak bisa ada 2 link yang sama.

---

## ❓ PERTANYAAN 2: Apakah data lama akan terhapus saat scraping baru?

### 🟢 TIDAK, data lama TIDAK akan terhapus!

**Penjelasan:**

1. **Scraper menggunakan `.insert()` bukan `.update()`**
   ```python
   # Ini APPEND (tambah) data baru
   response = self.supabase.table(table_name).insert(data_to_insert).execute()
   
   # Bukan REPLACE atau DELETE
   ```

2. **Apa yang terjadi saat scraping baru:**
   ```
   Scraping Lama:  [domain1, domain2, domain3]
   Disimpan ke DB: [domain1, domain2, domain3]
   
   Scraping Baru:  [domain2, domain4, domain5]
   Disimpan ke DB: [domain1, domain2, domain3, domain2*, domain4, domain5]
                                        ↑
                                   Di-skip (duplicate link constraint)
   
   Hasil akhir: [domain1, domain2, domain3, domain4, domain5]
                 └─ Lama ─┘└─ Baru ─┘
   ```

3. **Duplicate Detection:**
   - Jika LINK yang sama → DI-SKIP (error constraint)
   - Jika DOMAIN sama tapi LINK berbeda → DITERIMA (valid)

---

## 📊 HOW IT WORKS - Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    SCRAPING PROCESS                          │
└──────────────────────────────────────────────────────────────┘

1. SCRAPE
   ├─ Search: "machine learning"
   └─ Results: 20 links

2. DEDUPLICATE (Local)
   ├─ Remove duplicate links dari hasil DDG
   └─ Keep: ~18 links unique

3. FILTER DOMAINS
   ├─ Check: is_domain_excluded()
   ├─ Skip: twitter.com, facebook.com, play.google.com, etc
   └─ Keep: ~15 links (exclude filtered)

4. CHECK SUPABASE CONSTRAINT
   ├─ Query existing links in DB
   ├─ Filter out links yang sudah ada
   └─ Keep: ~12 NEW links (tidak ada di DB)

5. INSERT TO SUPABASE
   ├─ Insert 12 new entries
   ├─ On duplicate link → SKIP (error handling)
   └─ Result: 12 entries saved
                │
6. DATABASE
   ├─ Old data: TETAP ADA (tidak dihapus)
   ├─ New data: DITAMBAH (append)
   └─ Total: Old + New entries


┌──────────────────────────────────────────────────────────────┐
│                    RESULT: ACCUMULATIVE                      │
│                                                               │
│  After Scrape 1: 20 entries                                 │
│  After Scrape 2: 20 + 12 = 32 entries                       │
│  After Scrape 3: 32 + 15 = 47 entries                       │
│  ...                                                          │
│  After Scrape N: N × Average entries per scrape             │
│                                                               │
│  ✅ Data lama SELALU aman dan tidak dihapus                 │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎯 SCENARIO: Duplikat dari Query Berbeda

```
CASE: Duplikat domain tapi dari query berbeda

Scrape 1: Query "Python"
└─ Find: github.com/python/cpython
   Saved: github.com (query="Python")

Scrape 2: Query "Programming"
└─ Find: github.com/trending/python
   Saved: github.com (query="Programming")

DATABASE:
ID 1: github.com | link=.../cpython      | query="Python"
ID 2: github.com | link=.../trending     | query="Programming"

✅ VALID: Kedua entries di-keep karena link berbeda!
   Domain sama tapi URL berbeda = valid data untuk berbagai keyword

❌ INVALID: Jika link yang sama EXACT
   github.com/cpython disimpan 2x → Entry kedua di-skip
```

---

## 🛠️ CLEANUP STRATEGY

### Ketika perlu cleanup?

1. **Manual check:** Data sudah banyak & perlu housekeeping
2. **Development:** Habis testing & ingin fresh database
3. **Maintenance:** Rutin cleanup untuk keep database clean

### Execution:

```bash
# Step 1: Preview apa yang akan dihapus
python preview_duplicates.py

# Step 2: Lihat jumlah entries yang akan hilang
[*] Total entries yang bisa dihapus: X
[*] Entries yang akan di-keep: Y

# Step 3: Confirm & execute
python cleanup_duplicates.py
# Input: yes (untuk proceed)

# Step 4: Verify
python preview_duplicates.py
# Output: "Tidak ada duplikat!"
```

---

## ✅ SUMMARY

| Pertanyaan | Jawaban |
|-----------|---------|
| **Menghapus duplikat?** | `python cleanup_duplicates.py` (script auto-delete) |
| **Data lama dihapus?** | ❌ TIDAK, data lama TETAP |
| **Kenapa ada duplikat?** | ✅ NORMAL, dari query berbeda & link berbeda |
| **Perlu di-cleanup?** | ✅ Optional, hanya jika ada duplicate link |
| **Impact ke scraping baru?** | ❌ NONE, tetap append (tidak replace) |

---

## 🚀 RECOMMENDATION

**Status saat ini: NORMAL & HEALTHY**

Tidak perlu cleanup urgent karena:
- ✅ Setiap duplikat adalah dari query/link berbeda (valid)
- ✅ Database constraint mencegah duplicate link (protection)
- ✅ Data lama tidak akan pernah terhapus (safe)

**Action Items (Optional):**
1. Jalankan `preview_duplicates.py` untuk monitoring
2. Jalankan `cleanup_duplicates.py` jika ingin remove older entries
3. Lanjut scraping - sistem handle semua otomatis
