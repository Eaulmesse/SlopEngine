# SlopEngine Frontend

Next.js frontend for the SlopEngine authentication system with Shadcn UI.

## Features

- ✅ Modern UI with Shadcn components
- ✅ OAuth2 authentication flow (Google, GitHub)
- ✅ JWT token management
- ✅ Responsive design with Tailwind CSS
- ✅ Dashboard with user management
- ✅ API integration with FastAPI backend

## Getting Started

### 1. Install dependencies
```bash
npm install
```

### 2. Configure environment
Copy `.env.local.example` to `.env.local`:
```bash
cp .env.local.example .env.local
```

### 3. Start development server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
nextjs/
├── app/                    # Next.js App Router
│   ├── page.tsx           # Homepage with login
│   ├── dashboard/         # Protected dashboard
│   └── auth/callback/     # OAuth callback handler
├── components/            # React components
│   ├── ui/               # Shadcn UI components
│   └── auth/             # Authentication components
├── lib/                   # Utilities and API client
└── public/               # Static assets
```

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000`.

### Key API endpoints:
- `GET /auth/providers` - List OAuth providers
- `GET /auth/google` - Google OAuth flow
- `GET /auth/github` - GitHub OAuth flow
- `GET /users/me` - Get current user info
- `GET /users/` - List all users
- `POST /users/` - Create user

## OAuth Flow

1. User clicks "Continue with Google/GitHub"
2. Redirects to backend OAuth endpoint
3. Backend handles OAuth and redirects to `/auth/callback` with token
4. Frontend stores token and redirects to dashboard

## Development

### Adding Shadcn components
```bash
npx shadcn@latest add [component-name]
```

### Building for production
```bash
npm run build
npm start
```

## Backend Requirements

Ensure the FastAPI backend is running with:
- CORS enabled for `http://localhost:3000`
- OAuth providers configured (Google, GitHub)
- PostgreSQL database running

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Technologies

- **Next.js 15** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **Shadcn UI** - Component library
- **Lucide React** - Icons
- **FastAPI** - Backend API
