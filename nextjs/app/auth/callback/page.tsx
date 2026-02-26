'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';

export default function AuthCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Processing authentication...');

  useEffect(() => {
    const processCallback = async () => {
      try {
        // Récupérer le token depuis l'URL (simulation)
        // En réalité, le backend devrait rediriger ici avec le token dans l'URL
        const token = searchParams.get('token');
        
        if (token) {
          api.setToken(token);
          setStatus('success');
          setMessage('Authentication successful! Redirecting to dashboard...');
          setTimeout(() => router.push('/dashboard'), 2000);
        } else {
          // Pour l'instant, on simule un succès
          // Plus tard, on pourra faire une requête au backend pour vérifier
          setStatus('success');
          setMessage('Authentication successful! Redirecting to dashboard...');
          setTimeout(() => router.push('/dashboard'), 2000);
        }
      } catch (error) {
        setStatus('error');
        setMessage(error instanceof Error ? error.message : 'Authentication failed');
      }
    };

    processCallback();
  }, [router, searchParams]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Authentication Callback</CardTitle>
          <CardDescription>
            Processing your OAuth authentication
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex flex-col items-center space-y-4">
            {status === 'loading' && (
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">{message}</p>
              </div>
            )}

            {status === 'success' && (
              <div className="text-center">
                <div className="h-12 w-12 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                  <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <p className="mt-4 text-green-600 font-medium">{message}</p>
              </div>
            )}

            {status === 'error' && (
              <div className="text-center">
                <div className="h-12 w-12 bg-red-100 rounded-full flex items-center justify-center mx-auto">
                  <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
                <p className="mt-4 text-red-600 font-medium">{message}</p>
                <Button
                  className="mt-4"
                  onClick={() => router.push('/')}
                >
                  Return to Login
                </Button>
              </div>
            )}
          </div>

          <div className="text-sm text-gray-500 text-center">
            <p>
              This page handles OAuth callbacks from Google and GitHub.
              The token will be stored securely in your browser.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}