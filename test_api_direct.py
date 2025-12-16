#!/usr/bin/env python3
"""
Test direct de l'API pour voir ce qui se passe
"""

import os
from dotenv import load_dotenv
from main import KissaCore

load_dotenv()

# Simuler ce que fait api.py
print("🔧 Initialisation de KissaCore (comme dans api.py)...")
kissa = KissaCore()

print("\n🔍 Test de search_candidates via l'instance API...")
results = kissa.search_candidates("Apparat")

print(f"\n✅ Résultats : {len(results)} éléments")
if len(results) > 0:
    print(f"Premier résultat : {results[0]}")
else:
    print("❌ Liste vide !")
    print("\nVérification du token Discogs...")
    token = os.getenv('DISCOGS_TOKEN')
    if token:
        print(f"✅ Token présent (longueur: {len(token)})")
    else:
        print("❌ Token manquant !")

