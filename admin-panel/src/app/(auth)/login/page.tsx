'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function LoginPage() {
    const router = useRouter();

    useEffect(() => {
        // Redirect to /peler (new login route)
        router.replace('/peler');
    }, [router]);

    return null;
}
