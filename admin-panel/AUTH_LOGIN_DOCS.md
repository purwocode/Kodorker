# Admin Login System Documentation

## Overview
Dashboard sekarang dilengkapi dengan sistem login yang aman menggunakan JWT tokens dan HTTP-only cookies.

## Features
- ✅ Username/Password authentication
- ✅ JWT token-based sessions  
- ✅ HTTP-only cookies (secure against XSS)
- ✅ Protected routes dengan middleware
- ✅ Automatic session validation
- ✅ Logout functionality
- ✅ Redirect to login if session expired

## Default Credentials

**Username:** `admin`  
**Password:** `password123`

> ⚠️ **PENTING:** Ganti credentials ini sebelum production!

## How to Change Credentials

Edit `.env.local`:
```env
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
JWT_SECRET=your_random_secret_key
```

Restart server:
```bash
npm run dev
```

## File Structure

```
admin-panel/src/
├── app/
│   ├── (auth)/login/page.tsx          # Login page
│   ├── (protected)/
│   │   ├── layout.tsx                 # Protected layout dengan navbar & logout
│   │   └── dashboard/page.tsx         # Main dashboard
│   ├── api/
│   │   └── auth/
│   │       ├── login/route.ts        # POST /api/auth/login
│   │       └── logout/route.ts       # POST /api/auth/logout
│   ├── layout.tsx                     # Root layout
│   └── page.tsx                       # Redirect to /dashboard or /login
├── lib/
│   └── auth.ts                        # Auth utilities (JWT, cookies)
├── middleware.ts                      # Route protection middleware
└── .env.local                         # Environment variables
```

## Flow Diagram

```
User Access Root URL (/)
    ↓
Check Session Token
    ↓
    ├─ Has Valid Token → Redirect to /dashboard
    └─ No Token → Redirect to /login

Login Page
    ↓
User Enter Credentials
    ↓
POST /api/auth/login
    ↓
    ├─ Credentials Valid → Create JWT Token + Set Cookie → Redirect to /dashboard
    └─ Invalid → Show Error Message

Protected Routes (/dashboard, /api/stats)
    ↓
Middleware Checks Token
    ↓
    ├─ Valid Token → Allow Access
    └─ Invalid/Missing Token → Redirect to /login

User Click Logout
    ↓
POST /api/auth/logout
    ↓
Delete Auth Cookie
    ↓
Redirect to /login
```

## Security Features

1. **JWT Tokens**
   - Signed dengan secret key
   - Expiration time: 24 hours
   - Stored in HTTP-only cookies (tidak bisa diakses dari JavaScript)

2. **Middleware Protection**
   - Semua routes di `/dashboard` dan protected routes memerlukan valid token
   - Automatic redirect ke login jika token expired

3. **CSRF Protection**
   - SameSite cookies (`SameSite=Lax`)
   - Mencegah cookie dikirim ke cross-site requests

4. **No XSS Vulnerability**
   - HTTP-only cookies tidak bisa diakses dari client-side JavaScript
   - Login credentials tidak disimpan di localStorage/sessionStorage

## Deployment Notes

Sebelum deploy ke production:

1. **Generate secure secret keys:**
   ```bash
   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
   ```

2. **Update `.env.local` atau `.env.production`:**
   ```env
   ADMIN_USERNAME=your_secure_username
   ADMIN_PASSWORD=your_secure_password
   JWT_SECRET=your_64_char_random_secret
   ```

3. **Enable secure cookies:**
   ```typescript
   // middleware.ts sudah set secure: true untuk production
   secure: process.env.NODE_ENV === 'production'
   ```

4. **Use HTTPS:**
   - Cookies secure flag memerlukan HTTPS di production
   - Configure server dengan SSL/TLS certificate

5. **Set NODE_ENV:**
   ```bash
   export NODE_ENV=production
   npm run build
   npm run start
   ```

## Testing Login

### Manual Test
1. Buka http://localhost:3000
2. Will redirect ke `/login`
3. Enter: `admin` / `password123`
4. Click `🔐 LOGIN`
5. Will redirect ke `/dashboard`
6. Click `🔒 LOGOUT` button
7. Will redirect ke `/login`

### Test Invalid Credentials
1. Enter wrong username/password
2. See error message: "Username atau password salah"

### Test Session Expiration
1. Login successfully
2. Wait 24 hours (or manually delete auth_token cookie)
3. Refresh page → Redirect ke login

## API Endpoints

### POST /api/auth/login
**Request:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Login berhasil"
}
```

**Response (Error):**
```json
{
  "error": "Username atau password salah"
}
```

### POST /api/auth/logout
**Request:** (no body needed)

**Response:**
```json
{
  "success": true,
  "message": "Logout berhasil"
}
```

## Troubleshooting

### "Login page blinks then redirects"
- Middleware is checking session
- Normal behavior jika sudah authenticated

### "Cookie tidak tersimpan"
- Check browser DevTools → Application → Cookies
- Pastikan domain same-site
- Di development, gunakan `http://localhost:3000`

### "Token expired sebelum 24 jam"
- Cek `.env` `JWT_SECRET` value
- Restart server jika ada perubahan env

### "Cannot read property 'auth_token'"
- Check middleware.ts menjalankan dengan benar
- Pastikan `next.config.js` tidak disable middleware

## Next Steps

1. Integrate dengan Supabase table untuk user management (optional)
2. Add password reset functionality
3. Add user roles/permissions
4. Add session history/audit log
5. Implement 2FA (Two-Factor Authentication)
