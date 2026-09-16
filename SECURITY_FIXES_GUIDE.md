# Security Fixes: Implementation Guide
**Date:** 2026-09-17  
**Priority:** CRITICAL - Execute before team access

---

## 🔴 CRITICAL FIX #1: Remove Hardcoded Default Credentials

### Current Vulnerability
```typescript
// lib/auth.ts (DANGEROUS)
export async function validateCredentials(
    username: string,
    password: string
): Promise<boolean> {
    const adminUsername = process.env.ADMIN_USERNAME || 'admin';
    const adminPassword = process.env.ADMIN_PASSWORD || 'password123';
    
    return username === adminUsername && password === adminPassword;
}
```

**Risk:** If environment variables not set, login succeeds with `admin`/`password123`

### Fix
```typescript
// lib/auth.ts (SECURE)
export async function validateCredentials(
    username: string,
    password: string
): Promise<boolean> {
    const adminUsername = process.env.ADMIN_USERNAME;
    const adminPassword = process.env.ADMIN_PASSWORD;
    
    // Require both to be configured
    if (!adminUsername || !adminPassword) {
        throw new Error('Admin credentials not configured in environment variables');
    }
    
    return username === adminUsername && password === adminPassword;
}
```

### Test It
```bash
# Without .env set:
# Before: Login works with admin/password123 ❌
# After: Login fails with error message ✅
```

---

## 🔴 CRITICAL FIX #2: Change Default JWT Secret

### Current Vulnerability
```typescript
// auth.ts, middleware.ts, API routes
const secret = new TextEncoder().encode(
    process.env.JWT_SECRET || 'dorker-super-secret-key-change-in-production'
);
```

**Risk:** 
- Weak entropy (only 44 chars)
- Comment suggests changing but defaults to weak secret
- Could be brute-forced in seconds

### Fix

1. **Generate New Secret**
   ```bash
   # On Windows PowerShell:
   [Convert]::ToBase64String([System.Security.Cryptography.RNGCryptoServiceProvider]::new().GetBytes(32))
   
   # On Linux/Mac:
   openssl rand -base64 32
   
   # Example output:
   # aBcDeFgHiJkLmNoPqRsT+UV/WxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfG=
   ```

2. **Update .env**
   ```
   JWT_SECRET="aBcDeFgHiJkLmNoPqRsT+UV/WxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfG="
   ```

3. **Update Code (Remove Fallback)**
   ```typescript
   // auth.ts
   const secret = new TextEncoder().encode(process.env.JWT_SECRET!);
   if (!process.env.JWT_SECRET) {
       throw new Error('JWT_SECRET environment variable is required');
   }
   ```

4. **Never Commit .env**
   ```bash
   # Check if .env is in .gitignore
   cat .gitignore | grep ".env"
   
   # If not, add it:
   echo ".env" >> .gitignore
   echo ".env.local" >> .gitignore
   ```

---

## 🔴 CRITICAL FIX #3: Secure Telegram Bot Token

### Current Issue
```
Location: .env (may be visible in git history, logs, or env)
Exposure: Telegram Bot Token allows:
  - Sending messages to your chat
  - Accessing chat history
  - Creating/deleting chat groups
```

### Fix: Use Vercel Secrets (Production)

1. **Remove from .env**
   ```bash
   # Before:
   TELEGRAM_BOT_TOKEN="123456:ABCDefGHIJKLmnoPQRsTUVwxYZ"
   TELEGRAM_CHAT_ID="987654321"
   
   # After:
   # Don't set locally (only in Vercel)
   ```

2. **Set in Vercel Dashboard**
   ```
   Go to: https://vercel.com/dashboard/projects/your-project
   → Settings → Environment Variables
   
   Add:
   - Name: TELEGRAM_BOT_TOKEN
     Value: 123456:ABCDefGHIJKLmnoPQRsTUVwxYZ
     Environments: Production, Preview
   
   - Name: TELEGRAM_CHAT_ID
     Value: 987654321
     Environments: Production, Preview
   ```

3. **Test Locally**
   ```bash
   # Create .env.local (NOT committed to git)
   TELEGRAM_BOT_TOKEN="..."
   TELEGRAM_CHAT_ID="..."
   
   # Make sure .env.local is in .gitignore
   ```

---

## ⚠️ HIGH FIX #4: Add CSRF Protection (sameSite: strict)

### Current Issue
```typescript
response.cookies.set('auth_token', token, {
    sameSite: 'lax',  // ⚠️  Allows POST from cross-site
});
```

### Fix
```typescript
// auth.ts
response.cookies.set('auth_token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',  // ✅ Changed from 'lax'
    maxAge: 86400,
    path: '/',
});

// Similar fix in all other places setting cookies
```

### Impact
- **Before:** CSRF attack via form POST possible
- **After:** Cookie NOT sent on cross-site POST (fully protected)

---

## ⚠️ HIGH FIX #5: Add X-Frame-Options Header

### Add to Middleware
```typescript
// middleware.ts
export async function middleware(request: NextRequest) {
    // ... existing code ...
    
    const response = NextResponse.next();
    
    // Add security headers
    response.headers.set('X-Frame-Options', 'DENY');
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('X-XSS-Protection', '1; mode=block');
    
    return response;
}
```

### Impact
- Prevents clickjacking attacks (embedding dashboard in iframe)
- Prevents MIME-type sniffing

---

## 📋 MEDIUM PRIORITY: Add Rate Limiting

### Install Package
```bash
cd admin-panel
npm install @upstash/ratelimit redis
```

### Add to .env
```
UPSTASH_REDIS_REST_URL="https://..."
UPSTASH_REDIS_REST_TOKEN="..."
```

### Apply to Login Endpoint
```typescript
// lib/ratelimit.ts (new file)
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

export const loginRateLimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(5, '15 m'),  // 5 attempts per 15 min
  analytics: true,
  prefix: 'ratelimit:login',
});

// app/api/auth/login/route.ts
import { loginRateLimit } from '@/lib/ratelimit';

export async function POST(request: NextRequest) {
    const ip = request.headers.get('x-forwarded-for') || 'unknown';
    
    const { success } = await loginRateLimit.limit(ip);
    if (!success) {
        return NextResponse.json(
            { error: 'Too many login attempts. Try again later.' },
            { status: 429 }
        );
    }
    
    // ... rest of login code ...
}
```

---

## 🔧 Implementation Checklist

- [ ] **Critical #1:** Remove default credentials ('password123')
- [ ] **Critical #2:** Change JWT secret to 256-bit random
- [ ] **Critical #3:** Move Telegram tokens to Vercel secrets
- [ ] **Critical #4:** Add CSRF protection (sameSite: strict)
- [ ] **Critical #5:** Add X-Frame-Options header
- [ ] **Verify .env is in .gitignore**
- [ ] **Test with test_security_audit.py**
- [ ] **Commit changes to GitHub**
- [ ] **Update Vercel environment variables**
- [ ] **Test login in production**

---

## 🧪 Verification Steps

### Step 1: Test No Token
```bash
curl -X GET https://kodorker.vercel.app/api/stats

# Expected: 401 Unauthorized ✅
```

### Step 2: Test Invalid Token
```bash
curl -X GET https://kodorker.vercel.app/api/stats \
  -H "Cookie: auth_token=invalid"

# Expected: 401 Unauthorized ✅
```

### Step 3: Test Header Injection
```bash
curl -X GET https://kodorker.vercel.app/api/stats \
  -H "Authorization: Bearer eyJ..."

# Expected: 401 Unauthorized ✅
# (Authorization header should be ignored)
```

### Step 4: Test Login with New Credentials
```bash
# Should fail with old credentials
curl -X POST https://kodorker.vercel.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'

# Expected: 401 Unauthorized (old password no longer works) ✅
```

---

## ⚡ Quick Implementation (30 minutes)

**If you're in a hurry, do these first:**

1. Change JWT secret in .env (2 min)
2. Remove default credentials fallback (3 min)
3. Add sameSite: strict (2 min)
4. Add X-Frame-Options header (3 min)
5. Update Vercel secrets (10 min)
6. Test with security audit script (10 min)

```bash
# Quick test
cd d:\Legion\ SMTP\ v6.5\ Latest\DORKER
python test_security_audit.py
```

---

## 🔒 Result After Fixes

| Issue | Before | After |
|-------|--------|-------|
| **Default Credentials** | Works with admin/password123 | Requires .env setup |
| **JWT Secret** | Weak (44 chars) | Strong (256-bit) |
| **CSRF via POST** | ⚠️ Possible | ✅ Protected |
| **Clickjacking** | ⚠️ Possible | ✅ Protected |
| **Telegram Token** | Visible in .env | 🔒 Vercel secrets |
| **Rate Limiting** | ❌ None | ✅ 5 attempts/15min |

---

## 📚 References

- [OWASP: JWT Vulnerabilities](https://owasp.org/www-community/attacks/jwt)
- [OWASP: CSRF Prevention](https://owasp.org/www-community/attacks/csrf)
- [Next.js Security Best Practices](https://nextjs.org/docs/going-to-production/security)
- [jose: JWT Library Documentation](https://github.com/panva/jose)
