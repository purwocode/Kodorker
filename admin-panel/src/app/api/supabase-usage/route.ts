import { NextResponse } from 'next/server';

interface UsageMetric {
    egress: { usage: number; limit: number };
    database_size: { usage: number; limit: number };
    monthly_active_users: { usage: number; limit: number };
    storage_size: { usage: number; limit: number };
}

export async function GET() {
    try {
        const projectRef = process.env.NEXT_PUBLIC_SUPABASE_URL?.split('//')[1].split('.')[0];
        const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

        if (!projectRef || !serviceRoleKey) {
            return NextResponse.json(
                {
                    error: 'Supabase credentials not configured',
                    egress: { usage: 0, limit: 5 },
                    database_size: { usage: 0, limit: 500 },
                    monthly_active_users: { usage: 0, limit: 50000 },
                    storage_size: { usage: 0, limit: 1 },
                },
                { status: 200 }
            );
        }

        // Fetch usage statistics from Supabase Management API
        const response = await fetch(
            `https://api.supabase.com/v1/projects/${projectRef}/usage`,
            {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${serviceRoleKey}`,
                    'Content-Type': 'application/json',
                },
            }
        );

        if (!response.ok) {
            // Return fallback values if API fails
            return NextResponse.json({
                egress: { usage: 0, limit: 5 },
                database_size: { usage: 0, limit: 500 },
                monthly_active_users: { usage: 0, limit: 50000 },
                storage_size: { usage: 0, limit: 1 },
            });
        }

        const data = (await response.json()) as UsageMetric;

        return NextResponse.json({
            egress: {
                usage: Math.round((data.egress?.usage || 0) / (1024 * 1024 * 1024) * 100) / 100,
                limit: 5,
            },
            database_size: {
                usage: Math.round((data.database_size?.usage || 0) / (1024 * 1024) * 100) / 100,
                limit: 500,
            },
            monthly_active_users: {
                usage: data.monthly_active_users?.usage || 0,
                limit: 50000,
            },
            storage_size: {
                usage: Math.round((data.storage_size?.usage || 0) / (1024 * 1024 * 1024) * 100) / 100,
                limit: 1,
            },
        });
    } catch {
        // Return fallback values on error
        return NextResponse.json({
            egress: { usage: 0, limit: 5 },
            database_size: { usage: 0, limit: 500 },
            monthly_active_users: { usage: 0, limit: 50000 },
            storage_size: { usage: 0, limit: 1 },
        });
    }
}
