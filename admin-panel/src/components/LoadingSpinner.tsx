export default function LoadingSpinner() {
    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
                <div className="inline-flex items-center justify-center mb-4">
                    <div className="relative w-16 h-16">
                        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-cyan-500 border-r-purple-500 animate-spin" style={{ boxShadow: '0 0 20px rgba(0,255,255,0.8)' }}></div>
                        <div className="absolute inset-2 rounded-full border-4 border-transparent border-b-green-400 border-l-orange-500 animate-spin" style={{ animationDirection: 'reverse', boxShadow: '0 0 15px rgba(0,255,100,0.6)' }}></div>
                    </div>
                </div>
                <h3 className="mt-4 text-2xl font-bold font-mono text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-green-400" style={{ textShadow: '0 0 20px rgba(0,255,255,0.5)' }}>INITIALIZING...</h3>
                <p className="text-green-300 text-sm mt-2 font-mono" style={{ textShadow: '0 0 10px rgba(0,255,100,0.6)' }}>$ Connecting to Supabase...</p>
                <div className="mt-6 flex justify-center gap-2">
                    <span className="inline-block w-2 h-2 rounded-full bg-lime-400 animate-pulse" style={{ boxShadow: '0 0 10px rgba(0,255,100,0.8)' }}></span>
                    <span className="inline-block w-2 h-2 rounded-full bg-cyan-400 animate-pulse" style={{ boxShadow: '0 0 10px rgba(0,255,255,0.8)', animationDelay: '0.2s' }}></span>
                    <span className="inline-block w-2 h-2 rounded-full bg-purple-400 animate-pulse" style={{ boxShadow: '0 0 10px rgba(200,100,255,0.8)', animationDelay: '0.4s' }}></span>
                </div>
            </div>
        </div>
    );
}
