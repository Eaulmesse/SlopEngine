import { LoginForm } from '@/components/auth/login-form';

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 p-4">
      <div className="w-full max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
            Welcome to <span className="text-blue-600">SlopEngine</span>
          </h1>
          <p className="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
            A modern authentication system with OAuth2, bcrypt, and PostgreSQL.
            Built with FastAPI, Next.js, and Shadcn UI.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 items-center">
          <div className="space-y-6">
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold text-gray-800">
                Features
              </h2>
              <ul className="space-y-3">
                <li className="flex items-center">
                  <div className="h-2 w-2 bg-blue-500 rounded-full mr-3"></div>
                  <span>OAuth2 with Google & GitHub</span>
                </li>
                <li className="flex items-center">
                  <div className="h-2 w-2 bg-blue-500 rounded-full mr-3"></div>
                  <span>Secure bcrypt password hashing</span>
                </li>
                <li className="flex items-center">
                  <div className="h-2 w-2 bg-blue-500 rounded-full mr-3"></div>
                  <span>JWT token authentication</span>
                </li>
                <li className="flex items-center">
                  <div className="h-2 w-2 bg-blue-500 rounded-full mr-3"></div>
                  <span>PostgreSQL database with migrations</span>
                </li>
                <li className="flex items-center">
                  <div className="h-2 w-2 bg-blue-500 rounded-full mr-3"></div>
                  <span>Docker deployment ready</span>
                </li>
                <li className="flex items-center">
                  <div className="h-2 w-2 bg-blue-500 rounded-full mr-3"></div>
                  <span>Modern UI with Shadcn components</span>
                </li>
              </ul>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-medium text-blue-800 mb-2">
                Getting Started
              </h3>
              <p className="text-sm text-blue-700">
                1. Configure OAuth providers in the backend<br />
                2. Start PostgreSQL with Docker<br />
                3. Run database migrations<br />
                4. Start both frontend and backend servers
              </p>
            </div>
          </div>

          <div className="flex justify-center">
            <LoginForm />
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-gray-200 text-center">
          <p className="text-sm text-gray-500">
            Backend running on: <code className="bg-gray-100 px-2 py-1 rounded">localhost:8000</code><br />
            Frontend running on: <code className="bg-gray-100 px-2 py-1 rounded">localhost:3000</code>
          </p>
        </div>
      </div>
    </main>
  );
}
