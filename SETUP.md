# 🚀 DORKER - Setup Guide

**DuckDuckGo Scraper with Supabase Integration & Next.js Admin Dashboard**

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Scraper](#running-the-scraper)
5. [Running the Admin Panel](#running-the-admin-panel)
6. [Telegram Integration (Optional)](#telegram-integration-optional)
7. [Features](#features)

---

## Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **Supabase Account** - [Sign up free](https://supabase.com)
- **Telegram Bot** (optional) - [Create via @BotFather](https://t.me/botfather)

---

## Installation

### 1. Clone or Extract Project
```bash
cd "D:\Legion SMTP v6.5 Latest\DORKER"
```

### 2. Setup Python Environment

#### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### Linux/Mac
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Setup Admin Panel (Next.js)
```bash
cd admin-panel
npm install
cd ..
```

---

## Configuration

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up
2. Create a new project
3. Go to **Settings → API**
4. Copy these values:
   - `Project URL` → `SUPABASE_URL`
   - `Anon Public Key` → `SUPABASE_KEY` / `NEXT_PUBLIC_SUPABASE_KEY`
   - `Service Role Key` → `SUPABASE_SERVICE_ROLE_KEY`

### Step 2: Create Database Table (Automatic)

Run this SQL in Supabase SQL Editor:

```sql
-- Create search_results table
create table search_results (
  id bigint primary key generated always as identity,
  query text not null,
  title text not null,
  body text,
  domain text not null,
  link text unique not null,
  created_at timestamp default now()
);

-- Create indexes for better performance
create index idx_search_results_domain on search_results(domain);
create index idx_search_results_query on search_results(query);
create index idx_search_results_created_at on search_results(created_at);

-- Enable Row Level Security
alter table search_results enable row level security;

-- Create policy for anon access (read-only)
create policy "Allow anonymous read access"
  on search_results for select
  to anon
  using (true);

-- Create policy for service role (full access)
create policy "Allow service role full access"
  on search_results for all
  to service_role
  using (true);
```

### Step 3: Configure Environment Variables

Create `.env` file in project root:

```env
# Scraper Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Admin Panel Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Admin Credentials (CHANGE BEFORE PRODUCTION!)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-strong-password-here

# JWT Secret (Generate: openssl rand -base64 32)
JWT_SECRET=your-jwt-secret-here

# Telegram Bot (Optional)
TELEGRAM_BOT_TOKEN=your-bot-token-here
TELEGRAM_CHAT_ID=your-chat-id-here
```

For Admin Panel, also create `admin-panel/.env.local` with same values.

---

## Running the Scraper

### Quick Start - Interactive Mode

```bash
python ddg_scraper.py
```

This will start the **Infinite Search Mode**:
1. Enter initial query (e.g., "Python Programming")
2. Scraper automatically extracts keywords from results
3. Uses keywords as next query
4. Continues until you press `CTRL+C`
5. Saves all results to Supabase automatically

### Programmatic Usage

```python
from ddg_scraper import DuckDuckGoScraper

# Create scraper instance
scraper = DuckDuckGoScraper("Your Search Query")

# Scrape results
results = scraper.scrape(max_results=20)

# Print results
scraper.print_results(limit=10)

# Save to Supabase
scraper.save_to_supabase()

# Or save to file
scraper.save_json('results.json')
scraper.save_csv('results.csv')
scraper.save_txt('results.txt')
```

### Features

✅ **No Bot Detection** - Uses DDGS library, no proxy needed
✅ **Subdomain Exclusion** - Automatically excludes subdomains of blocked sites
✅ **Duplicate Prevention** - Tracks seen domains and URLs
✅ **Infinite Search** - Auto-generates queries from results
✅ **Supabase Integration** - Direct database storage
✅ **Multiple Export Formats** - JSON, CSV, TXT

---

## Running the Admin Panel

### Development Mode

```bash
cd admin-panel
npm run dev
```

Visit: `http://localhost:3000`

**Login Credentials:**
- Username: `admin`
- Password: (from `.env.local`)

### Production Build

```bash
cd admin-panel
npm run build
npm start
```

### Deploy to Vercel

```bash
cd admin-panel
npm run build
vercel --prod
```

### Features

✅ **Real-time Stats** - Total domains, results, queries
✅ **Supabase Metrics** - Live usage: Egress, Database Size, Storage, Active Users
✅ **Domain Table** - Browse all scraped domains
✅ **Download Domains** - Export as `.txt` file
✅ **Telegram Integration** - Send domains to Telegram bot
✅ **Authentication** - JWT-based login system
✅ **Cyberpunk Theme** - Neon green/cyan aesthetic

---

## Telegram Integration (Optional)

### Setup

1. **Create Telegram Bot**
   - Chat with [@BotFather](https://t.me/botfather)
   - Send `/newbot`
   - Follow prompts
   - Copy `BOT_TOKEN`

2. **Get Chat ID**
   - Chat with [@userinfobot](https://t.me/userinfobot)
   - Send any message
   - Copy `User ID`

3. **Configure Environment**
   
   Update `.env` and `admin-panel/.env.local`:
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZ
   TELEGRAM_CHAT_ID=987654321
   ```

4. **Test**
   
   Click "📤 SEND TO TELEGRAM" button in dashboard to send domains as `.txt` file

---

## Project Structure

```
DORKER/
├── ddg_scraper.py           # Main scraper class
├── requirements.txt         # Python dependencies
├── .env                     # Environment configuration
├── run_both.sh/bat          # Scripts to run scraper + panel
├── README.md                # Project overview
├── SETUP.md                 # This file
└── admin-panel/
    ├── src/
    │   ├── app/             # Next.js app directory
    │   │   ├── page.tsx     # Public homepage
    │   │   ├── (protected)/
    │   │   │   └── dashboard/page.tsx  # Admin dashboard
    │   │   ├── api/         # API routes
    │   │   │   ├── stats/
    │   │   │   ├── supabase-usage/
    │   │   │   ├── telegram/
    │   │   │   └── auth/
    │   │   └── layout.tsx   # Root layout
    │   ├── components/      # React components
    │   ├── lib/             # Utilities
    │   └── middleware.ts    # JWT validation
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── next.config.ts
    └── .env.local           # Local environment

```

---

## Troubleshooting

### Python Issues

**"No module named 'ddgs'"**
```bash
pip install duckduckgo-search
```

**"No module named 'supabase'"**
```bash
pip install supabase python-postgrest
```

**UnicodeEncodeError (Windows)**
```powershell
$env:PYTHONIOENCODING="utf-8"
python ddg_scraper.py
```

### Next.js Issues

**"npm: command not found"**
- Install Node.js from https://nodejs.org/

**"Port 3000 already in use"**
```bash
npm run dev -- -p 3001
```

**"Cannot find module '@supabase/supabase-js'"**
```bash
cd admin-panel
npm install
```

### Supabase Issues

**"Table search_results not found"**
- Run the SQL setup script in Supabase SQL Editor

**"Invalid API key"**
- Check `.env` values match Supabase project settings
- Regenerate keys if needed

**"RLS policy denied"**
- Verify RLS policies are created (see SQL setup)

### Telegram Issues

**"Telegram credentials not configured"**
- Fill `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`

**"Bad Request: can't parse entities"**
- Already fixed! Plain text caption format is used

---

## Security Notes

⚠️ **BEFORE PRODUCTION:**

1. **Change default credentials**
   ```env
   ADMIN_USERNAME=your-unique-username
   ADMIN_PASSWORD=your-strong-password
   ```

2. **Rotate JWT Secret**
   ```bash
   # Generate new secret
   openssl rand -base64 32
   ```

3. **Rotate Supabase Keys**
   - Go to Supabase Settings → API
   - Click "Rotate keys" for both anon and service role

4. **Never commit `.env` files**
   - Already in `.gitignore`
   - Double-check before pushing

5. **Use HTTPS in production**
   - Vercel automatically provides HTTPS
   - Ensure `secure` flag in JWT cookie config

6. **Restrict IP addresses** (optional)
   - Supabase Dashboard → Settings → Network
   - Add your server IPs to allowlist

---

## Quick Commands

```bash
# Activate Python environment
.venv\Scripts\Activate.ps1

# Run scraper (interactive)
python ddg_scraper.py

# Run admin panel (dev)
cd admin-panel && npm run dev

# Build admin panel
cd admin-panel && npm run build

# Deploy to Vercel
cd admin-panel && vercel --prod

# Run both simultaneously (if using run_both.bat)
run_both.bat
```

---

## Support

- **Supabase Docs:** https://supabase.com/docs
- **Next.js Docs:** https://nextjs.org/docs
- **DuckDuckGo Search:** https://www.duckduckgo.com
- **Telegram Bot API:** https://core.telegram.org/bots

---

## License

This project is for educational purposes.

---

**Last Updated:** 2026-09-16
**Version:** 1.0.0
