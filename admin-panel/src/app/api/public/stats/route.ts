import { NextRequest, NextResponse } from 'next/server';

interface SearchResult {
    domain: string;
    query: string;
    title: string;
}

/**
 * Public API endpoint - Returns only aggregated stats (counts)
 * No authentication required
 * Endpoint: GET /api/public/stats
 *
 * Response:
 * {
 *   "total_domains": 844,
 *   "total_results": 1000,
 *   "total_queries": 220,
 *   "unique_titles": 981
 * }
 */
export async function GET(request: NextRequest) {
    try {
        // Initialize Supabase client
        const { createClient } = await import('@supabase/supabase-js');

        const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
        const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_KEY;

        if (!supabaseUrl || !supabaseKey) {
            return NextResponse.json(
                { error: 'Service unavailable' },
                { status: 503 }
            );
        }

        const supabase = createClient(supabaseUrl, supabaseKey);

        // Fetch ONLY the necessary fields for counting
        const { data: results, error } = await supabase
            .from('search_results')
            .select('domain, query, title');

        if (error) throw error;

        // Calculate stats from raw data
        const totalResults = results?.length || 0;
        const uniqueDomains = new Set((results as SearchResult[])?.map((r) => r.domain) || []);
        const uniqueQueries = new Set((results as SearchResult[])?.map((r) => r.query) || []);
        const uniqueTitles = new Set((results as SearchResult[])?.map((r) => r.title) || []);

        // Return ONLY aggregated stats, no actual data
        return NextResponse.json(
            {
                total_domains: uniqueDomains.size,
                total_results: totalResults,
                total_queries: uniqueQueries.size,
                unique_titles: uniqueTitles.size,
            },
            {
                headers: {
                    'Cache-Control': 'public, max-age=300', // Cache for 5 minutes
                    'Access-Control-Allow-Origin': '*', // Allow cross-origin requests
                },
            }
        );
    } catch (error) {
        console.error('Error fetching public stats:', error);
        return NextResponse.json(
            {
                error: 'Failed to fetch statistics',
                total_domains: 0,
                total_results: 0,
                total_queries: 0,
                unique_titles: 0,
            },
            { status: 500 }
        );
    }
}
