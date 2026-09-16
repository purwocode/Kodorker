import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

// Verify JWT token from cookies
async function verifyAuth(request: NextRequest) {
    const token = request.cookies.get('auth_token')?.value;

    if (!token) {
        return { valid: false, error: 'Unauthorized: No authentication token' };
    }

    try {
        const secret = new TextEncoder().encode(
            process.env.JWT_SECRET || 'dorker-super-secret-key-change-in-production'
        );
        await jwtVerify(token, secret);
        return { valid: true };
    } catch (error) {
        return { valid: false, error: 'Unauthorized: Invalid token' };
    }
}

export async function POST(request: NextRequest) {
    // Verify authentication first
    const auth = await verifyAuth(request);
    if (!auth.valid) {
        return NextResponse.json(
            { error: auth.error },
            { status: 401 }
        );
    }

    try {
        const { domains, count } = await request.json();

        if (!domains || domains.length === 0) {
            return NextResponse.json(
                { error: 'No domains to send' },
                { status: 400 }
            );
        }

        const botToken = process.env.TELEGRAM_BOT_TOKEN;
        const chatId = process.env.TELEGRAM_CHAT_ID;

        if (!botToken || !chatId) {
            console.error('Missing Telegram credentials:', { botToken: !!botToken, chatId: !!chatId });
            return NextResponse.json(
                { error: 'Telegram credentials not configured. Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env.local' },
                { status: 500 }
            );
        }

        // Create file content
        const timestamp = new Date().toISOString().split('T')[0];
        const fileContent = domains.join('\n');
        const fileName = `domains_${timestamp}.txt`;

        // Create FormData using native Node.js support
        const formData = new FormData();

        // Add fields
        formData.append('chat_id', chatId);
        formData.append('caption',
            `DORKER - Domain Export\n\n` +
            `Date: ${timestamp}\n` +
            `Total Domains: ${count}\n` +
            `File: ${fileName}`
        );
        // Removed parse_mode to avoid Markdown entity parsing errors

        // Create file blob and append
        const fileBlob = new Blob([fileContent], { type: 'text/plain' });
        formData.append('document', fileBlob, fileName);

        // Send to Telegram
        const telegramUrl = `https://api.telegram.org/bot${botToken}/sendDocument`;
        console.log('Sending to Telegram:', {
            telegramUrl: telegramUrl.replace(botToken, '***'),
            chatId,
            fileName,
            domainCount: count
        });

        const telegramResponse = await fetch(telegramUrl, {
            method: 'POST',
            body: formData,
        });

        const responseText = await telegramResponse.text();
        console.log('Telegram response:', {
            status: telegramResponse.status,
            body: responseText.substring(0, 200)
        });

        if (!telegramResponse.ok) {
            console.error('Telegram API error:', { status: telegramResponse.status, response: responseText });
            try {
                const errorData = JSON.parse(responseText);
                return NextResponse.json(
                    { error: `Telegram API error: ${errorData.description || responseText}` },
                    { status: 500 }
                );
            } catch {
                return NextResponse.json(
                    { error: `Telegram API error: ${responseText}` },
                    { status: 500 }
                );
            }
        }

        const result = JSON.parse(responseText);
        return NextResponse.json({
            success: true,
            message: `✅ Sent ${count} domains as file to Telegram`,
            telegram_message_id: result.result.message_id,
            file_name: fileName,
        });
    } catch (err) {
        console.error('Telegram send error:', err);
        return NextResponse.json(
            {
                error: err instanceof Error ? err.message : 'Unknown error',
                details: err instanceof Error ? err.stack : 'No stack trace'
            },
            { status: 500 }
        );
    }
}
