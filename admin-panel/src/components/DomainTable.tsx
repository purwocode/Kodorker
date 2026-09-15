export default function DomainTable({
    results,
}: {
    results: Array<{
        id: number;
        domain: string;
        title: string;
        query: string;
        created_at: string;
    }>;
}) {
    if (results.length === 0) {
        return (
            <div className="bg-gray-950 border-2 border-purple-500 rounded p-12 text-center" style={{ boxShadow: '0 0 20px rgba(200,100,255,0.2), inset 0 0 10px rgba(200,100,255,0.05)' }}>
                <p className="text-purple-300 font-mono text-lg" style={{ textShadow: '0 0 10px rgba(200,100,255,0.6)' }}>[ AWAITING DATA ] • No results yet • Start scraping to initialize stream</p>
            </div>
        );
    }

    return (
        <div className="bg-gray-950 border-2 border-cyan-500 rounded overflow-hidden" style={{ boxShadow: '0 0 20px rgba(0,255,255,0.3), inset 0 0 10px rgba(0,255,255,0.1)' }}>
            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="bg-gray-900 border-b-2 border-green-500">
                            <th className="px-6 py-4 text-left text-xs font-mono font-bold text-green-400 uppercase tracking-widest" style={{ textShadow: '0 0 10px rgba(0,255,100,0.7)' }}>Domain</th>
                            <th className="px-6 py-4 text-left text-xs font-mono font-bold text-green-400 uppercase tracking-widest" style={{ textShadow: '0 0 10px rgba(0,255,100,0.7)' }}>Title</th>
                            <th className="px-6 py-4 text-left text-xs font-mono font-bold text-green-400 uppercase tracking-widest" style={{ textShadow: '0 0 10px rgba(0,255,100,0.7)' }}>Query</th>
                            <th className="px-6 py-4 text-left text-xs font-mono font-bold text-green-400 uppercase tracking-widest" style={{ textShadow: '0 0 10px rgba(0,255,100,0.7)' }}>Timestamp</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-cyan-900">
                        {results.map((result, idx) => (
                            <tr key={result.id} className="hover:bg-gray-800 transition-colors group" style={{ backgroundColor: idx % 2 === 0 ? 'rgba(0,0,0,0.2)' : 'rgba(0,255,255,0.03)' }}>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <a
                                        href={`https://${result.domain}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-cyan-400 hover:text-lime-300 font-mono text-sm font-bold transition-colors group-hover:underline"
                                        style={{ textShadow: '0 0 10px rgba(0,255,255,0.5)' }}
                                    >
                                        → {result.domain}
                                    </a>
                                </td>
                                <td className="px-6 py-4">
                                    <p className="text-green-300 text-sm truncate max-w-xs font-mono" style={{ textShadow: '0 0 8px rgba(0,255,100,0.4)' }}>{result.title}</p>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className="inline-flex items-center px-3 py-1 rounded font-mono text-xs font-bold bg-gray-800 text-purple-300 border border-purple-500" style={{ boxShadow: '0 0 10px rgba(200,100,255,0.4)' }}>
                                        #{result.query}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-orange-400 font-mono" style={{ textShadow: '0 0 8px rgba(255,165,0,0.4)' }}>
                                    {new Date(result.created_at).toLocaleDateString()} {new Date(result.created_at).toLocaleTimeString()}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="bg-gray-900 px-6 py-4 border-t-2 border-purple-500">
                <p className="text-sm text-purple-300 font-mono" style={{ textShadow: '0 0 10px rgba(200,100,255,0.5)' }}>[ STREAM ACTIVE ] Displaying <span className="text-lime-400 font-bold">{results.length}</span> Results</p>
            </div>
        </div>
    );
}
