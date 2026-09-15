import { NextRequest, NextResponse } from 'next/server';
import { validateCredentials, createToken } from '@/lib/auth';

export async function POST(request: NextRequest) {
    try {
        const { username, password } = await request.json();

        if (!username || !password) {
            return NextResponse.json(
                { error: 'Username dan password diperlukan' },
                { status: 400 }
            );
        }

        const isValid = await validateCredentials(username, password);

        if (!isValid) {
            return NextResponse.json(
                { error: 'Username atau password salah' },
                { status: 401 }
            );
        }

        // Create JWT token
        const token = await createToken(username);

        // Set cookie
        const response = NextResponse.json({ success: true, message: 'Login berhasil' });
        response.cookies.set('auth_token', token, {
            httpOnly: true,
            secure: process.env.NODE_ENV === 'production',
            sameSite: 'lax',
            maxAge: 86400,
            path: '/',
        });

        return response;
    } catch (error) {
        console.error('Login error:', error);
        return NextResponse.json(
            { error: 'Terjadi kesalahan server' },
            { status: 500 }
        );
    }
}
