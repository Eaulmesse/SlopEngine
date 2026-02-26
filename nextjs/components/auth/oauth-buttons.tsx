'use client';

import { Button } from '@/components/ui/button';
import { Github, Mail } from 'lucide-react';
import { api } from '@/lib/api';

export function OAuthButtons() {
  const handleOAuthLogin = async (provider: string) => {
    await api.loginWithOAuth(provider);
  };

  return (
    <div className="space-y-4">
      <Button
        type="button"
        variant="outline"
        className="w-full"
        onClick={() => handleOAuthLogin('google')}
      >
        <Mail className="mr-2 h-4 w-4" />
        Continue with Google
      </Button>
      <Button
        type="button"
        variant="outline"
        className="w-full"
        onClick={() => handleOAuthLogin('github')}
      >
        <Github className="mr-2 h-4 w-4" />
        Continue with GitHub
      </Button>
    </div>
  );
}