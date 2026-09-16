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
        pathname === '/api/auth/logout' ||
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
        // For API endpoints, return 401 instead of redirecting
        if (pathname.startsWith('/api/')) {
            return NextResponse.json(
                { error: 'Unauthorized: No authentication token' },
                { status: 401 }
            );
        }
        // For page routes, redirect to login
        return NextResponse.redirect(new URL('/peler', request.url));
    }

    try {
        await jwtVerify(token, secret);
        return NextResponse.next();
    } catch {
        // For API endpoints, return 401 instead of redirecting
        if (pathname.startsWith('/api/')) {
            return NextResponse.json(
                { error: 'Unauthorized: Invalid or expired token' },
                { status: 401 }
            );
        }
        // For page routes, redirect to login
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
