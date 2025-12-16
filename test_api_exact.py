#!/usr/bin/env python3
"""
Test qui simule EXACTEMENT ce que fait l'endpoint API
"""

import os
import sys

# Simuler l'import comme dans api.py
from dotenv import load_dotenv
load_dotenv()

from main import KissaCore

# Simuler l'initialisation comme dans api.py (ligne 58)
print("=" * 60)
print("SIMULATION EXACTE DE L'API")
print("=" * 60)
print()

print("🔧 Initialisation de KissaCore (comme api.py ligne 58)...")
kissa = KissaCore()
print("✅ KissaCore initialisé")
print()

# Simuler l'endpoint /search-candidates
print("🔍 Simulation de l'endpoint /search-candidates...")
print("-" * 60)

query = sys.argv[1] if len(sys.argv) > 1 else "Apparat"

try:
    print(f"📥 Requête reçue pour la recherche : '{query}'")
    print(f"📥 Type de la requête : str")
    print(f"📥 Query value : {query}")
    
    print(f"🔍 Test direct avec kissa.search_candidates...")
    results = kissa.search_candidates(query)
    print(f"📤 Résultats obtenus : {len(results)} éléments, type: {type(results)}")
    
    if len(results) == 0:
        print("⚠️ ATTENTION : Liste vide retournée par search_candidates")
        # Test avec une requête fixe pour voir si c'est la requête qui pose problème
        test_results = kissa.search_candidates("Apparat")
        print(f"🧪 Test avec 'Apparat' : {len(test_results)} résultats")
    
    # S'assurer que les résultats sont sérialisables en JSON
    serializable_results = []
    for result in results:
        try:
            serializable_result = {
                "discogs_id": int(result.get("discogs_id", 0)) if result.get("discogs_id") else 0,
                "title": str(result.get("title", "")),
                "artist": str(result.get("artist", "")),
                "year": str(result.get("year", "")),
                "label": str(result.get("label", "")),
                "thumb": str(result.get("thumb", ""))
            }
            serializable_results.append(serializable_result)
        except Exception as item_error:
            print(f"⚠️ Erreur sérialisation item : {item_error}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"📤 Résultats sérialisés : {len(serializable_results)} éléments")
    
    if len(serializable_results) > 0:
        print(f"\n✅ PREMIER RÉSULTAT SÉRIALISÉ :")
        import json
        print(json.dumps(serializable_results[0], indent=2, ensure_ascii=False))
    else:
        print("\n❌ AUCUN RÉSULTAT SÉRIALISÉ")
        
except Exception as e:
    print(f"❌ Erreur dans la simulation : {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)

