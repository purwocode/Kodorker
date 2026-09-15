# 🚀 Scraper Admin Panel - Setup Guide

Admin dashboard untuk memonitor hasil DuckDuckGo scraper secara real-time.

## 📋 Quick Start

### 1. Install Dependencies
```bash
npm install
# atau
npm install @supabase/supabase-js
```

### 2. Setup Environment Variables

Buat file `.env.local` di root folder admin-panel:

```env
NEXT_PUBLIC_SUPABASE_URL=https://fomkvkjdvhgovpzkucvc.supabase.co
NEXT_PUBLIC_SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZvbWt2a2pkdmhnb3ZwemtVY3ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MjczMTEsImV4cCI6MjA0MjEwMzMxMX0.w4X-gxsXk0L0bVW8-8V4dB2-q8E5-J0G-K9L-M8N-O9P
```

> ⚠️ Ganti dengan credentials Supabase Anda sendiri!

### 3. Run Development Server

```bash
npm run dev
```

Buka [http://localhost:3000](http://localhost:3000) di browser.

---

## 📊 Features

### Dashboard Stats
- **Total Domains** 🌐 - Unique domains yang terambil
- **Total Results** 📊 - Total hasil scraping
- **Queries Executed** 🔍 - Jumlah queries yang dijalankan
- **Unique Titles** 📝 - Jumlah title unik

### Recent Results Table
- Menampilkan 10 hasil terbaru
- Link ke domain (clickable)
- Query yang digunakan
- Timestamp kapan di-scrape
- Auto-refresh setiap 30 detik

### Monitoring
- Live data dari Supabase
- Real-time statistics
- Beautiful UI dengan Tailwind CSS

---

## 🔧 Architecture

```
admin-panel/
├── src/
│   ├── app/
│   │   ├── page.tsx           (Dashboard page)
│   │   ├── layout.tsx         (Root layout)
│   │   └── api/
│   │       └── stats/
│   │           └── route.ts   (Fetch stats from Supabase)
│   └── components/
│       ├── StatsCard.tsx      (Stats display)
│       ├── DomainTable.tsx    (Results table)
│       └── LoadingSpinner.tsx (Loading state)
├── .env.local                 (Environment variables)
├── package.json
├── tsconfig.json
└── tailwind.config.ts
```

---

## 📡 API Routes

### GET /api/stats
Fetch semua statistics dari Supabase.

**Response:**
```json
{
  "total_domains": 45,
  "total_results": 150,
  "total_queries": 5,
  "unique_titles": 120,
  "recent_results": [
    {
      "id": 1,
      "domain": "example.com",
      "title": "Example Title",
      "query": "artificial intelligence",
      "created_at": "2026-09-16T10:30:00Z"
    }
  ]
}
```

---

## 🎨 Customization

### Ubah Refresh Interval
Di `page.tsx`, ubah nilai di `setInterval`:
```typescript
const interval = setInterval(fetchStats, 30000);  // 30 detik
```

### Ubah Limit Recent Results
Di `route.ts`, ubah `.slice(0, 10)`:
```typescript
const recentResults = (results || [])
  .slice(0, 20)  // Ubah ke 20
```

### Ubah Styling
Edit Tailwind classes di components. Configurasi ada di `tailwind.config.ts`.

---

## 🚀 Deployment

### Deploy ke Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Deploy ke Other Platforms
Next.js compatible dengan:
- Netlify
- AWS Amplify
- Railway
- DigitalOcean
- Heroku

---

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_KEY` | Supabase public key (anon) |

> 💡 Prefix `NEXT_PUBLIC_` membuat variable accessible di browser (safe untuk public key)

---

## 🐛 Troubleshooting

### Error: "Supabase credentials not configured"
- ✅ Pastikan `.env.local` sudah dibuat
- ✅ Pastikan variable names benar
- ✅ Restart dev server (`npm run dev`)

### Data tidak muncul
- ✅ Cek Supabase connection di console
- ✅ Pastikan table `search_results` sudah ada di Supabase
- ✅ Pastikan ada data di table (run scraper dulu)

### Styling tidak jalan
- ✅ Pastikan Tailwind CSS terinstall: `npm install -D tailwindcss`
- ✅ Clear cache: `rm -rf .next && npm run dev`

---

## 📚 Resources

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [React Docs](https://react.dev)

---

## 📝 Scripts

```bash
npm run dev       # Start development server
npm run build     # Build for production
npm run start     # Run production build
npm run lint      # Run ESLint
```

---

## 📄 License

MIT

---

**Happy monitoring! 🎉**
