# FastAPI User CRUD avec Bcrypt et OAuth2

API CRUD complète pour la gestion des utilisateurs avec authentification bcrypt et OAuth2.

## Fonctionnalités

- ✅ CRUD complet pour les utilisateurs
- ✅ Hachage bcrypt pour les mots de passe
- ✅ Validation email avec Pydantic
- ✅ Base de données PostgreSQL avec SQLAlchemy
- ✅ Migrations avec Alembic
- ✅ Docker Compose pour le déploiement
- ✅ OAuth2 avec Google et GitHub
- ✅ Tokens JWT pour l'authentification

## Installation

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Configuration de la base de données
Copiez le fichier `.env.example` en `.env` et modifiez les variables :
```bash
cp .env.example .env
```

### 3. Configuration OAuth2
Configurez les providers OAuth2 (Google et GitHub) :
- Suivez les instructions dans `oauth_config.md`
- Ajoutez vos Client ID et Client Secret dans le fichier `.env`

### 4. Lancer PostgreSQL avec Docker
```bash
docker-compose up -d postgres
```

### 4. Exécuter les migrations
```bash
alembic upgrade head
```

### 5. Démarrer l'API
```bash
uvicorn main:app --reload
```

## Endpoints API

### Utilisateurs
- `POST /users/` - Créer un utilisateur
- `GET /users/{id}` - Récupérer un utilisateur
- `GET /users/` - Lister les utilisateurs
- `PUT /users/{id}` - Mettre à jour un utilisateur
- `DELETE /users/{id}` - Supprimer un utilisateur

### OAuth2
- `GET /auth/providers` - Liste des providers OAuth disponibles
- `GET /auth/google` - Authentification Google
- `GET /auth/google/callback` - Callback Google (retourne token JWT)
- `GET /auth/github` - Authentification GitHub
- `GET /auth/github/callback` - Callback GitHub (retourne token JWT)

### Modèles

#### UserCreate (POST/PUT)
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### UserResponse (GET)
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

## Structure du projet
```
fastapi/
├── main.py              # Application principale
├── auth.py              # Authentification bcrypt
├── oauth.py             # Authentification OAuth2
├── oauth_config.md      # Configuration OAuth2
├── requirements.txt     # Dépendances Python
├── alembic/            # Migrations de base de données
├── docker-compose.yml  # Configuration Docker
├── Dockerfile          # Build Docker
└── .env.example        # Variables d'environnement
```

## Déploiement avec Docker
```bash
docker-compose up -d
```

L'API sera disponible sur `http://localhost:8000`

## Documentation API
Une fois l'API démarrée, accédez à :
- `http://localhost:8000/docs` - Documentation interactive Swagger
- `http://localhost:8000/redoc` - Documentation Redoc