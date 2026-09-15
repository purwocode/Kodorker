import { cookies } from 'next/headers';
import { jwtVerify, SignJWT } from 'jose';

const secret = new TextEncoder().encode(
    process.env.JWT_SECRET || 'dorker-super-secret-key-change-in-production'
);

export interface AuthToken {
    username: string;
    iat: number;
}

export async function createToken(username: string): Promise<string> {
    const token = await new SignJWT({ username })
        .setProtectedHeader({ alg: 'HS256' })
        .setIssuedAt()
        .setExpirationTime('24h')
        .sign(secret);
    return token;
}

export async function verifyToken(token: string): Promise<AuthToken | null> {
    try {
        const verified = await jwtVerify(token, secret);
        return verified.payload as unknown as AuthToken;
    } catch {
        return null;
    }
}

export async function setAuthCookie(token: string): Promise<void> {
    const cookieStore = await cookies();
    cookieStore.set('auth_token', token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 86400, // 24 hours
        path: '/',
    });
}

export async function getAuthCookie(): Promise<string | undefined> {
    const cookieStore = await cookies();
    return cookieStore.get('auth_token')?.value;
}

export async function clearAuthCookie(): Promise<void> {
    const cookieStore = await cookies();
    cookieStore.delete('auth_token');
}

export async function validateCredentials(
    username: string,
    password: string
): Promise<boolean> {
    const adminUsername = process.env.ADMIN_USERNAME || 'admin';
    const adminPassword = process.env.ADMIN_PASSWORD || 'password123';

    return username === adminUsername && password === adminPassword;
}

export async function getSession(): Promise<AuthToken | null> {
    const token = await getAuthCookie();
    if (!token) return null;
    return verifyToken(token);
}
