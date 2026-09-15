import { NextRequest, NextResponse } from 'next/server';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export async function POST(_request: NextRequest) {
    const response = NextResponse.json({ success: true, message: 'Logout berhasil' });
    response.cookies.delete('auth_token');
    return response;
}
