-- Supabase SQL Schema untuk DuckDuckGo Scraper
-- Buat table untuk menyimpan hasil pencarian

-- 1. Buat table search_results
CREATE TABLE IF NOT EXISTS search_results (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    query TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    domain TEXT NOT NULL,
    link TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 2. Create index untuk query dan domain (untuk pencarian cepat)
CREATE INDEX IF NOT EXISTS idx_search_query ON search_results(query);
CREATE INDEX IF NOT EXISTS idx_search_domain ON search_results(domain);
CREATE INDEX IF NOT EXISTS idx_search_created_at ON search_results(created_at);

-- 3. Enable Row Level Security (optional, untuk keamanan)
ALTER TABLE search_results ENABLE ROW LEVEL SECURITY;

-- 4. Create policy untuk read access (allow all)
CREATE POLICY "Allow read access" ON search_results
    FOR SELECT USING (true);

-- 5. Create policy untuk insert access (allow all)
CREATE POLICY "Allow insert access" ON search_results
    FOR INSERT WITH CHECK (true);

-- Alternatif: Jika ingin lebih restrictive, gunakan authentication:
-- CREATE POLICY "Allow authenticated insert" ON search_results
--     FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Query contoh untuk menggunakan table:
-- SELECT * FROM search_results WHERE query = 'Python' ORDER BY created_at DESC;
-- SELECT DISTINCT domain FROM search_results WHERE query = 'Web API Design';
-- SELECT * FROM search_results WHERE created_at > NOW() - INTERVAL '7 days';
