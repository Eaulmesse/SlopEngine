# Configuration OAuth2

## Configuration des providers

### Google OAuth2
1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez l'API "Google+"
4. Créez des identifiants OAuth 2.0
5. Configurez l'écran de consentement OAuth
6. Ajoutez l'URI de redirection : `http://localhost:8000/auth/google/callback`
7. Copiez le Client ID et Client Secret dans `.env`

### GitHub OAuth2
1. Allez sur [GitHub Developer Settings](https://github.com/settings/developers)
2. Cliquez sur "New OAuth App"
3. Remplissez les informations :
   - Application name : Votre nom d'application
   - Homepage URL : `http://localhost:3000`
   - Authorization callback URL : `http://localhost:8000/auth/github/callback`
4. Copiez le Client ID et Client Secret dans `.env`

## Variables d'environnement requises

```env
# Google
GOOGLE_CLIENT_ID=votre-client-id-google
GOOGLE_CLIENT_SECRET=votre-client-secret-google

# GitHub
GITHUB_CLIENT_ID=votre-client-id-github
GITHUB_CLIENT_SECRET=votre-client-secret-github

# Frontend
FRONTEND_URL=http://localhost:3000
```

## Endpoints OAuth2

### 1. Liste des providers disponibles
```
GET /auth/providers
```

### 2. Authentification Google
```
GET /auth/google
```
Redirige vers l'écran de connexion Google

### 3. Callback Google
```
GET /auth/google/callback
```
Retourne un token JWT après authentification réussie

### 4. Authentification GitHub
```
GET /auth/github
```
Redirige vers l'écran de connexion GitHub

### 5. Callback GitHub
```
GET /auth/github/callback
```
Retourne un token JWT après authentification réussie

## Réponse du token
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "123456789",
    "email": "user@example.com",
    "name": "John Doe",
    "picture": "https://...",
    "provider": "google"
  }
}
```

## Utilisation du token
Ajoutez le token dans les headers des requêtes :
```
Authorization: Bearer <access_token>
```

## Sécurité
- Les tokens expirent après 30 minutes
- Utilisez HTTPS en production
- Stockez les secrets dans des variables d'environnement
- Régénérez les secrets régulièrement