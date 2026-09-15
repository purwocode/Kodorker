# Admin Login System - Quick Start Guide

## 🚀 Apa yang Baru?

Dashboard sekarang memiliki **sistem login** yang aman! Semua orang harus login dengan credentials sebelum bisa akses dashboard.

## 🔐 Default Credentials

```
Username: admin
Password: password123
```

## 📋 Fitur-Fitur

✅ **Login Page** dengan tema hacker  
✅ **JWT Token** untuk authentication  
✅ **HTTP-Only Cookies** untuk security  
✅ **Protected Routes** via middleware  
✅ **Logout Button** di navbar  
✅ **Session Validation** otomatis  

## 🎯 How It Works

```
Buka http://localhost:3000
    ↓
Redirect ke /login (karena belum login)
    ↓
Enter username & password
    ↓
Click 🔐 LOGIN
    ↓
Create JWT token → Set cookie → Redirect ke /dashboard
    ↓
Dashboard siap dengan data
    ↓
Click 🔒 LOGOUT di navbar
    ↓
Delete cookie → Redirect ke /login
```

## 🔄 Test Workflow

### 1. Start Development Server
```bash
cd admin-panel
npm run dev
```

### 2. Access Dashboard
- Open: http://localhost:3000
- Akan redirect ke login page

### 3. Login dengan Default Credentials
- Username: `admin`
- Password: `password123`
- Click: `🔐 LOGIN`

### 4. View Dashboard
- Sekarang bisa lihat dashboard dengan data scraper
- Navy bar atas: `[DORKER_DASHBOARD]` dengan logout button

### 5. Logout
- Click: `🔒 LOGOUT`
- Akan redirect ke login page

## 🔧 Ganti Credentials

Edit `.env.local`:
```env
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
JWT_SECRET=your_secret_key
```

Restart server:
```bash
# Stop (Ctrl+C)
npm run dev
```

## 📁 File Structure Baru

```
src/
├── app/
│   ├── (auth)/login/page.tsx        ← Login page
│   ├── (protected)/
│   │   ├── layout.tsx               ← Navbar dengan logout
│   │   └── dashboard/page.tsx       ← Main dashboard
│   ├── api/auth/
│   │   ├── login/route.ts           ← Login endpoint
│   │   └── logout/route.ts          ← Logout endpoint
│   ├── layout.tsx                   ← Root layout
│   └── page.tsx                     ← Redirect logic
├── lib/auth.ts                      ← Auth utilities
├── middleware.ts                    ← Route protection
└── .env.local                       ← Credentials
```

## 🎨 UI/UX

### Login Page
- Dark theme dengan neon glow
- Hacker aesthetic konsisten
- Error messages dengan red neon borders
- System status indicator

### Dashboard
- Navy bar atas: `[DORKER_DASHBOARD]`
- Logout button di kanan dengan red glow
- Semua fitur dashboard tetap sama

## ⚠️ Important for Production

Sebelum production:

1. **Ganti default credentials!**
   ```env
   ADMIN_USERNAME=something_secure
   ADMIN_PASSWORD=very_long_random_password
   ```

2. **Generate random JWT secret:**
   ```bash
   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
   ```

3. **Use environment variables:**
   - Jangan commit `.env.local` ke git
   - Use `.env.production` di server
   - Set via process.env di deployment platform

4. **Enable HTTPS:**
   - Cookies secure flag requires HTTPS
   - Deploy dengan SSL/TLS certificate

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Login page blinks | Normal - checking session |
| Cannot login | Check credentials di `.env.local` |
| Session expired immediately | Check JWT_SECRET value |
| Redirect loop | Clear browser cookies |
| 404 on login | Restart `npm run dev` |

## 📚 Documentation

Untuk detailed documentation:
- Buka: `AUTH_LOGIN_DOCS.md`
- Covers: Security, Flow Diagram, API Endpoints, Deployment

## ✨ Next Features

Optional enhancements:
- [ ] Add user registration
- [ ] Add password reset
- [ ] Add user roles
- [ ] Add 2FA (Two-Factor Authentication)
- [ ] Add session history logs
- [ ] Integrate with database for users

---

**Questions?** Check `AUTH_LOGIN_DOCS.md` untuk full documentation!
