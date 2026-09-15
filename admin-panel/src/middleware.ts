import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

const secret = new TextEncoder().encode(
    process.env.JWT_SECRET || 'dorker-super-secret-key-change-in-production'
);

export async function middleware(request: NextRequest) {
    const token = request.cookies.get('auth_token')?.value;
    const pathname = request.nextUrl.pathname;

    // Public routes - jangan perlu auth
    const isPublicRoute =
        pathname === '/' ||
        pathname === '/peler' ||
        pathname === '/api/auth/login' ||
        pathname === '/api/auth/logout' ||  // BUG FIX: logout should be public
        pathname === '/api/stats' ||
        pathname === '/api/supabase-usage' ||  // BUG FIX: metrics should be public
        pathname.startsWith('/_next') ||
        pathname.startsWith('/static') ||
        pathname === '/favicon.ico';

    if (isPublicRoute) {
        return NextResponse.next();
    }

    // Protected routes - butuh auth
    const isProtectedRoute = pathname.startsWith('/dashboard') || pathname.startsWith('/api/');

    if (!isProtectedRoute) {
        return NextResponse.next();
    }

    // Check token for protected routes
    if (!token) {
        return NextResponse.redirect(new URL('/peler', request.url));
    }

    try {
        await jwtVerify(token, secret);
        return NextResponse.next();
    } catch {
        return NextResponse.redirect(new URL('/peler', request.url));
    }
}

export const config = {
    matcher: [
        /*
         * Match all request paths except for the ones starting with:
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico (favicon file)
         */
        '/((?!_next/static|_next/image|favicon.ico).*)',
    ],
};
