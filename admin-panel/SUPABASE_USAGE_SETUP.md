# Supabase Usage Metrics Setup

Dashboard kini menampilkan **real-time Supabase infrastructure metrics** termasuk:
- 📊 **Egress** (0 / 5 GB)
- 🗄️ **Database Size** (26 / 500 MB)  
- 👥 **Monthly Active Users** (0 / 50,000)
- 💾 **File Storage** (0 / 1 GB)

## Setup Instructions

### 1️⃣ Get Supabase Service Role Key

1. Buka **[Supabase Dashboard](https://app.supabase.com)**
2. Pilih project Anda: `fomkvkjdvhgovpzkucvc`
3. Masuk ke **Settings** → **API**
4. Cari **Service Role Key** (Secret key - jangan gunakan Anon key)
5. Copy key tersebut (dimulai dengan `eyJhbGciOiJ...`)

### 2️⃣ Add ke .env.local

Edit file `.env.local` di folder admin-panel:

```env
# Supabase Management API (for usage statistics)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZvbWt2a2pkdmhnb3Zwemt1Y3ZjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4OTQ5NTQxNSwiZXhwIjoyMTA1MDcxNDE1fQ...
```

⚠️ **PENTING**: Jangan share key ini ke public atau Git!

### 3️⃣ Restart Development Server

```bash
npm run dev
```

### 4️⃣ Verify Setup

Buka browser dan kunjungi:
- http://localhost:3000 (public dashboard)
- Atau http://localhost:3000/dashboard (protected)

Anda akan melihat **"SUPABASE_INFRASTRUCTURE"** section di bagian atas dengan 4 metric cards yang menampilkan:
- Real-time usage data
- Progress bars dengan color coding:
  - 🟢 **Green**: < 70% usage
  - 🟠 **Orange**: 70-89% usage  
  - 🔴 **Red**: ≥ 90% usage

## API Endpoint

Dashboard menggunakan endpoint API baru:

```
GET /api/supabase-usage
```

**Response Format:**
```json
{
  "egress": { "usage": 0.5, "limit": 5 },
  "database_size": { "usage": 26, "limit": 500 },
  "monthly_active_users": { "usage": 0, "limit": 50000 },
  "storage_size": { "usage": 0.1, "limit": 1 }
}
```

**Units:**
- `egress`: GB (Gigabytes)
- `database_size`: MB (Megabytes)
- `monthly_active_users`: Count
- `storage_size`: GB (Gigabytes)

## Features

✅ **Real-time Monitoring** - Data refresh setiap 30 detik  
✅ **Visual Indicators** - Progress bars dengan color coding  
✅ **Fallback Mode** - Jika Service Role Key tidak dikonfigurasi, tampil nilai default (0)  
✅ **Responsive Design** - Bekerja di mobile, tablet, desktop  
✅ **Cyberpunk Theme** - Mengikuti desain hacker aesthetic dashboard  

## Troubleshooting

### Metrics Showing 0 Values

1. **Cek .env.local** - Pastikan `SUPABASE_SERVICE_ROLE_KEY` ada dan benar
2. **Restart server** - Jalankan `npm run dev` ulang
3. **Check browser console** - Buka DevTools untuk melihat error

### "Invalid API key" Error

- Pastikan menggunakan **Service Role Key**, bukan Anon Key
- Service Role Key lebih panjang dan dimulai dengan format JWT yang berbeda

### No Metrics Display

- Jika Service Role Key tidak dikonfigurasi, endpoint akan return default values
- Setup Service Role Key untuk menampilkan real data dari Supabase

## Security Notes

🔒 **Never commit Service Role Key ke Git!**

1. Service Role Key ada di `.gitignore` (file `.env.local`)
2. Gunakan environment variable saat deploy ke production
3. Rotate key secara berkala dari Supabase Dashboard
4. Service Role Key hanya boleh digunakan di backend (server-only), tidak di client

## How It Works

1. Dashboard component (`page.tsx`) melakukan `fetch('/api/supabase-usage')`
2. Backend endpoint (`api/supabase-usage/route.ts`) memanggil **Supabase Management API**
3. API mengembalikan usage statistics dalam format yang sudah diformat (GB, MB, count)
4. Data ditampilkan dengan `UsageStats` component
5. Auto-refresh setiap 30 detik (sama dengan scraper stats)

---

**Status:** ✅ Ready to use  
**Last Updated:** 2026-09-16  
**API Version:** Supabase Management API v1
