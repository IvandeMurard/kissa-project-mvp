#!/usr/bin/env python3
"""
Script de test pour diagnostiquer la recherche de candidats
Affiche tous les logs et détails de la recherche
"""

import os
from dotenv import load_dotenv
from main import KissaCore

# Charger les variables d'environnement
load_dotenv()

def test_search(query="Apparat"):
    """Teste la recherche avec affichage détaillé des logs"""
    
    print("=" * 60)
    print(f"TEST DE RECHERCHE : '{query}'")
    print("=" * 60)
    print()
    
    # Initialiser le moteur
    print("🔧 Initialisation du moteur Kissa...")
    try:
        kissa = KissaCore()
        print("✅ Moteur initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        return
    print()
    
    # Lancer la recherche
    print(f"🔍 Lancement de la recherche pour : '{query}'")
    print("-" * 60)
    
    try:
        results = kissa.search_candidates(query)
        
        print()
        print("=" * 60)
        print("RÉSULTATS")
        print("=" * 60)
        print(f"Nombre de résultats trouvés : {len(results)}")
        print()
        
        if len(results) == 0:
            print("⚠️  AUCUN RÉSULTAT TROUVÉ")
            print()
            print("Diagnostics possibles :")
            print("1. Vérifiez que DISCOGS_TOKEN est défini dans le .env")
            print("2. Vérifiez votre connexion internet")
            print("3. Vérifiez que le token Discogs est valide")
            print("4. Tous les résultats ont peut-être été filtrés")
        else:
            print("📋 Détails des résultats :")
            print()
            for i, candidate in enumerate(results, 1):
                print(f"  {i}. {candidate.get('title', 'N/A')}")
                print(f"     Artiste: {candidate.get('artist', 'N/A')}")
                print(f"     Année: {candidate.get('year', 'N/A')}")
                print(f"     Label: {candidate.get('label', 'N/A')}")
                print(f"     ID Discogs: {candidate.get('discogs_id', 'N/A')}")
                print(f"     Image: {'Oui' if candidate.get('thumb') else 'Non'}")
                print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERREUR CRITIQUE")
        print("=" * 60)
        print(f"Type d'erreur : {type(e).__name__}")
        print(f"Message : {str(e)}")
        print()
        import traceback
        print("Traceback complet :")
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("FIN DU TEST")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    
    # Permettre de passer une requête en argument
    query = sys.argv[1] if len(sys.argv) > 1 else "Apparat"
    
    test_search(query)

