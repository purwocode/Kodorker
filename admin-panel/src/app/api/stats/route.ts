import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

interface SearchResult {
    id: number;
    domain: string;
    query: string;
    title: string;
    body: string;
    link: string;
    created_at: string;
}

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

export async function GET(request: NextRequest) {
    // Verify authentication first
    const auth = await verifyAuth(request);
    if (!auth.valid) {
        return NextResponse.json(
            { error: auth.error },
            { status: 401 }
        );
    }

    try {
        // Initialize Supabase client
        const { createClient } = await import('@supabase/supabase-js');

        const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
        const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_KEY;

        if (!supabaseUrl || !supabaseKey) {
            return NextResponse.json(
                { error: 'Supabase credentials not configured' },
                { status: 500 }
            );
        }

        const supabase = createClient(supabaseUrl, supabaseKey);

        // Fetch all results
        const { data: results, error } = await supabase
            .from('search_results')
            .select('*')
            .order('created_at', { ascending: false });

        if (error) throw error;

        // Calculate stats
        const totalResults = results?.length || 0;
        const uniqueDomains = new Set((results as SearchResult[])?.map((r) => r.domain) || []);
        const uniqueQueries = new Set((results as SearchResult[])?.map((r) => r.query) || []);
        const uniqueTitles = new Set((results as SearchResult[])?.map((r) => r.title) || []);

        // Get recent results (limit to 1000 for display/download)
        const recentResults = ((results as SearchResult[]) || [])
            .slice(0, 1000)
            .map((r) => ({
                id: r.id,
                domain: r.domain,
                title: r.title,
                query: r.query,
                created_at: r.created_at,
            }));

        return NextResponse.json({
            total_domains: uniqueDomains.size,
            total_results: totalResults,
            total_queries: uniqueQueries.size,
            unique_titles: uniqueTitles.size,
            recent_results: recentResults,
        });
    } catch (error) {
        console.error('Error fetching stats:', error);
        return NextResponse.json(
            {
                error: error instanceof Error ? error.message : 'Failed to fetch stats',
                total_domains: 0,
                total_results: 0,
                total_queries: 0,
                unique_titles: 0,
                recent_results: [],
            },
            { status: 500 }
        );
    }
}
