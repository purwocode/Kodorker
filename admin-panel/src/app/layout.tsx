import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DORKER - Scraper Terminal",
  description: "DuckDuckGo scraper monitoring system",
  icons: {
    icon: '/favicon.svg',
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-black text-green-400" style={{ backgroundImage: 'radial-gradient(circle at 20% 50%, rgba(0,255,136,0.1) 0%, transparent 50%)', backgroundAttachment: 'fixed' }}>
        {/* Scanlines effect */}
        <div className="fixed inset-0 pointer-events-none opacity-5" style={{ backgroundImage: 'repeating-linear-gradient(0deg, #000, #000 2px, transparent 2px, transparent 4px)' }}></div>

        {/* Header */}
        <header className="bg-black border-b-2 border-cyan-500 sticky top-0 z-50 shadow-lg" style={{ boxShadow: '0 0 20px rgba(0,255,255,0.5), inset 0 0 20px rgba(0,255,255,0.1)' }}>
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <div className="flex items-center gap-3 mb-2">

              <h1 className="text-4xl font-bold font-mono text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-green-400 to-purple-500">
                [ DORKING MONITOR ]
              </h1>

            </div>
            <p className="text-green-300 mt-1 text-sm font-mono" style={{ textShadow: '0 0 10px rgba(0,255,100,0.7)' }}>
              &gt; DuckDuckGo Scraper Monitoring System | Real-time Data Stream
            </p>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 max-w-7xl mx-auto w-full py-6 px-4 sm:px-6 lg:px-8 relative z-10">
          {children}
        </main>

        {/* Footer */}
        <footer className="bg-black border-t-2 border-purple-500" style={{ boxShadow: '0 0 20px rgba(200,100,255,0.3), inset 0 0 20px rgba(200,100,255,0.05)' }}>
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 text-center">
            <p className="text-purple-300 text-sm font-mono" style={{ textShadow: '0 0 10px rgba(200,100,255,0.7)' }}>
              DORKER MONITOR | Powered by Purwocode | Status: ONLINE 🟢
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
