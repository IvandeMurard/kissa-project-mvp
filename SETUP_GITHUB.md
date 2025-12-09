# Instructions pour publier sur GitHub

## 1. Créer le repository sur GitHub

1. Allez sur https://github.com
2. Cliquez sur **+** (en haut à droite) → **New repository**
3. Remplissez :
   - **Repository name** : `kissa-project-mvp`
   - **Description** : `Application de gestion de collection vinyle avec OCR, Discogs et Spotify`
   - **Visibilité** : Public ou Private (selon votre choix)
   - **⚠️ IMPORTANT** : NE PAS cocher "Add a README file" (on a déjà un README)
4. Cliquez sur **Create repository**

## 2. Lier votre projet local au repository GitHub

Ouvrez PowerShell dans le dossier `kissa` et exécutez :

```powershell
# Se placer dans le dossier kissa
cd C:\Users\IVAN\Documents\kissa

# Ajouter le remote GitHub (remplacez VOTRE_USERNAME)
git remote add origin https://github.com/VOTRE_USERNAME/kissa-project-mvp.git

# Renommer la branche en 'main' (si ce n'est pas déjà fait)
git branch -M main

# Pousser le code sur GitHub
git push -u origin main
```

## 3. Vérification

Allez sur https://github.com/VOTRE_USERNAME/kissa-project-mvp et vérifiez que tous les fichiers sont présents.

## Notes importantes

- ⚠️ Les fichiers sensibles (`.env`, `*.key`, `*.json` de credentials) sont exclus par `.gitignore`
- ⚠️ Ne commitez JAMAIS vos clés API ou tokens
- ✅ Le `.gitignore` est configuré pour exclure automatiquement les fichiers sensibles

