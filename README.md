# Kissa - Application de Gestion de Collection Vinyle 🎵

Application web pour scanner, rechercher et gérer votre collection de vinyles avec OCR, intégration Discogs et Spotify.

## 🚀 Fonctionnalités

- **📸 Scan OCR** : Reconnaissance automatique du texte sur les pochettes avec Google Vision API
- **🔍 Recherche manuelle** : Recherche textuelle avec sélection parmi les candidats trouvés
- **🎨 Interface moderne** : Design responsive et intuitif
- **💾 Base de données** : Sauvegarde dans Supabase
- **🎵 Intégration Spotify** : Liens vers les albums et pochettes haute résolution
- **📚 Métadonnées complètes** : Artiste, titre, année, label, tracklist

## 📁 Structure du Projet

```
kissa/
├── backend/          # API FastAPI (Python)
│   ├── main.py      # Moteur principal (OCR, Discogs, Spotify)
│   ├── api.py       # Endpoints FastAPI
│   └── ...
├── frontend/         # Interface Next.js (React/TypeScript)
│   ├── src/app/     # Pages et composants
│   └── ...
└── README.md
```

## 🛠️ Installation

### Prérequis

- Python 3.8+
- Node.js 18+
- Comptes API :
  - Google Cloud (Vision API)
  - Discogs API
  - Spotify API
  - Supabase

### Configuration

1. **Backend** :
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Frontend** :
   ```bash
   cd frontend
   npm install
   ```

3. **Variables d'environnement** :
   - Créez un fichier `.env` dans `backend/` avec :
     ```
     GOOGLE_APPLICATION_CREDENTIALS=path/to/kissa-vision-key.json
     DISCOGS_TOKEN=votre_token_discogs
     SPOTIFY_CLIENT_ID=votre_client_id
     SPOTIFY_CLIENT_SECRET=votre_client_secret
     SUPABASE_URL=votre_url_supabase
     SUPABASE_KEY=votre_cle_supabase
     ```

## 🚀 Démarrage

### Option 1 : Script automatique (Recommandé)
Double-cliquez sur `start-all.bat` pour lancer les deux serveurs.

### Option 2 : Démarrage manuel

**Backend (port 8000) :**
```bash
cd backend
.\start-server.bat
```

**Frontend (port 3000) :**
```bash
cd frontend
.\start-frontend.bat
```

## 🌐 Accès

- **Frontend** : http://localhost:3000
- **Backend API** : http://127.0.0.1:8000
- **Documentation API** : http://127.0.0.1:8000/docs

## 📖 Utilisation

1. **Scan automatique** : Cliquez sur "Scan", prenez une photo de la pochette
2. **Recherche manuelle** : Cliquez sur "Clavier", tapez le nom de l'artiste/album
3. **Sélection** : Choisissez parmi les résultats proposés
4. **Ajout** : L'album est automatiquement ajouté à votre collection

## 🏗️ Technologies

- **Backend** : FastAPI, Python, Google Vision API, Discogs API, Spotify API
- **Frontend** : Next.js 16, React, TypeScript, Tailwind CSS
- **Base de données** : Supabase (PostgreSQL)

## 📝 Licence

MIT

## 👤 Auteur

IVAN
