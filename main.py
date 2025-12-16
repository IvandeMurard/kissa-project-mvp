import os

import json

from dotenv import load_dotenv



# Clients APIs

from google.cloud import vision

import discogs_client

import spotipy

from spotipy.oauth2 import SpotifyClientCredentials



# Chargement des variables d'environnement

load_dotenv()



class KissaCore:

    """

    Le moteur central de Kissa. 

    Gère l'OCR, la récupération de métadonnées et le lien streaming.

    """

    

    def __init__(self):

        # 1. Setup Google Vision

        # Google cherche automatiquement la variable 'GOOGLE_APPLICATION_CREDENTIALS' dans l'OS

        # ou le fichier JSON défini dans le .env

        try:
            # Vérifier si les credentials sont disponibles
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if credentials_path and os.path.exists(credentials_path):
                self.vision_client = vision.ImageAnnotatorClient()
            elif os.path.exists('kissa-vision-key.json'):
                # Fallback: chercher le fichier local
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'kissa-vision-key.json'
                self.vision_client = vision.ImageAnnotatorClient()
            else:
                print("⚠️ Attention : GOOGLE_APPLICATION_CREDENTIALS non configuré. OCR désactivé.")
                self.vision_client = None
        except Exception as e:
            print(f"⚠️ Attention : Erreur lors de l'initialisation de Google Vision : {e}. OCR désactivé.")
            self.vision_client = None

        

        # 2. Setup Discogs

        user_token = os.getenv('DISCOGS_TOKEN')

        if not user_token:

            print("⚠️ Attention : DISCOGS_TOKEN manquant dans le .env")

        self.discogs = discogs_client.Client('KissaApp/1.0', user_token=user_token)

        

        # 3. Setup Spotify

        client_id = os.getenv('SPOTIPY_CLIENT_ID')

        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

        if client_id and client_secret:

            auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

            self.sp = spotipy.Spotify(auth_manager=auth_manager)

        else:

            print("⚠️ Attention : Identifiants Spotify manquants dans le .env")

            self.sp = None



    def _clean_text(self, text):

        """Nettoie le texte brut de l'OCR pour la recherche"""

        return text.replace("\n", " ").strip()



    def step_1_ocr(self, image_path):

        """Lit le texte sur la pochette (Google Vision)"""

        if not self.vision_client:
            print("⚠️ OCR non disponible : Google Vision credentials manquants")
            return None

        print(f"👁️  Analyse visuelle de {image_path}...")

        try:

            with open(image_path, "rb") as image_file:

                content = image_file.read()

            image = vision.Image(content=content)

            response = self.vision_client.text_detection(image=image)
            
            # Vérification des erreurs de l'API
            if response.error.message:
                print(f"❌ Erreur Google Vision : {response.error.message}")
                return None

            texts = response.text_annotations

            if texts:

                raw_text = texts[0].description

                clean_query = self._clean_text(raw_text)

                print(f"📝 Texte détecté : {clean_query}")

                return clean_query

            else:

                return None

        except Exception as e:

            print(f"❌ Erreur OCR : {e}")

            return None



    def step_2_discogs(self, query):

        """Récupère les métadonnées (Discogs)"""

        print("💿 Recherche Discogs...")

        try:

            results = self.discogs.search(query, type='release')

            

            if not results:

                return None

            

            # On prend le premier résultat pertinent

            album = results[0]

            

            # Sécurisation des champs (au cas où il manque une info)

            if album.artists:

                # On joint tous les noms trouvés (ex: "Floating Points, Pharoah Sanders, LSO")

                artist_name = ", ".join([artist.name for artist in album.artists])

            else:

                artist_name = "Artiste Inconnu"

            label_name = album.labels[0].name if album.labels else "Label Inconnu"

            cover_url = album.images[0]['uri'] if album.images else None

            

            # On filtre la tracklist pour éviter les titres de faces (ex: "Side A")

            clean_tracklist = [t.title for t in album.tracklist if t.position]



            return {

                "artist": artist_name,

                "album_title": album.title,

                "year": str(album.year) if album.year else "Année inconnue",

                "label": label_name,

                "genre": album.genres,

                "tracklist": clean_tracklist,

                "discogs_url": album.url,

                "discogs_image": cover_url

            }

        except Exception as e:

            print(f"❌ Erreur Discogs: {e}")

            return None



    def step_3_spotify(self, artist, album_title):

        """Récupère le lien audio et la cover HD (Spotify)"""

        if not self.sp:

            return None

            

        print("🎵 Recherche Spotify...")

        q = f"artist:{artist} album:{album_title}"

        

        try:

            results = self.sp.search(q=q, type='album', limit=1)

            items = results['albums']['items']

            

            if items:

                spotify_album = items[0]

                # Spotify classe les images par taille, index 0 = la plus grande (640x640)

                hd_cover = spotify_album['images'][0]['url'] if spotify_album['images'] else None

                

                return {

                    "spotify_link": spotify_album['external_urls']['spotify'],

                    "spotify_uri": spotify_album['uri'],

                    "cover_hd": hd_cover

                }

            return None

        except Exception as e:

            print(f"⚠️ Erreur Spotify (non bloquant) : {e}")

            return None



    def process(self, image_path):

        """Orchestre tout le processus et formate pour le Frontend"""

        

        # 1. VISION

        detected_text = self.step_1_ocr(image_path)

        if not detected_text:

            return {"status": "error", "message": "Texte illisible sur la photo."}

            

        # 2. DATA

        discogs_data = self.step_2_discogs(detected_text)

        if not discogs_data:

            return {"status": "error", "message": "Album introuvable sur Discogs avec ce texte."}

            

        # 3. AUDIO & VISUAL

        spotify_data = self.step_3_spotify(discogs_data['artist'], discogs_data['album_title'])

        

        # 4. CONSTRUCTION DE L'OBJET FINAL

        # Logique : On préfère l'image Spotify (souvent plus propre/carrée), sinon Discogs

        final_cover = discogs_data['discogs_image']

        spotify_link = None

        spotify_uri = None

        

        if spotify_data:

            spotify_link = spotify_data['spotify_link']

            spotify_uri = spotify_data['spotify_uri']

            if spotify_data['cover_hd']:

                final_cover = spotify_data['cover_hd']



        # Structure optimisée pour ton Frontend React

        final_record = {

            "status": "success",

            "display": {

                "artist": discogs_data['artist'],

                "title": discogs_data['album_title'],

                "cover_image": final_cover, # L'image officielle propre

                "original_photo": image_path # On garde la trace locale si besoin

            },

            "details": {

                "year": discogs_data['year'],

                "label": discogs_data['label'],

                "genre": discogs_data['genre'],

                "tracklist": discogs_data['tracklist']

            },

            "links": {

                "spotify_url": spotify_link,

                "spotify_uri": spotify_uri,

                "discogs_url": discogs_data['discogs_url']

            }

        }

        

        return final_record



    def search_by_text(self, text_query):

        """Recherche manuelle sans image (texte -> Discogs -> Spotify)"""

        print(f"🔎 Recherche manuelle pour : {text_query}")

        

        # 1. Discogs (Directement avec le texte utilisateur)

        discogs_data = self.step_2_discogs(text_query)

        if not discogs_data:

            return {"status": "error", "message": "Album introuvable sur Discogs."}

            

        # 2. Spotify

        spotify_data = self.step_3_spotify(discogs_data['artist'], discogs_data['album_title'])

        

        # 3. Construction objet final (Idem process classique)

        final_cover = discogs_data['discogs_image']

        spotify_link = None

        spotify_uri = None

        

        if spotify_data:

            spotify_link = spotify_data['spotify_link']

            spotify_uri = spotify_data['spotify_uri']

            if spotify_data['cover_hd']:

                final_cover = spotify_data['cover_hd']

        return {

            "status": "success",

            "display": {

                "artist": discogs_data['artist'],

                "title": discogs_data['album_title'],

                "cover_image": final_cover,

                "original_photo": None # Pas de photo en mode manuel

            },

            "details": {

                "year": discogs_data['year'],

                "label": discogs_data['label'],

                "genre": discogs_data['genre'],

                "tracklist": discogs_data['tracklist']

            },

            "links": {

                "spotify_url": spotify_link,

                "spotify_uri": spotify_uri,

                "discogs_url": discogs_data['discogs_url']

            }

        }



    def search_candidates(self, query):

        """Recherche 'Google Style' : Tolérante et robuste"""

        print(f"🔎 Recherche robuste pour : {query}")

        

        try:

            # 1. Recherche large sur Discogs

            # On demande explicitement les types 'release' et 'master' pour éviter

            # de récupérer trop d'artistes ou de labels qui polluent, 

            # mais on reste assez large pour trouver les albums par nom d'artiste.

            results = self.discogs.search(query, type='release')

            # Note: Si on met type='all', Discogs renvoie l'artiste en premier.

            # En mettant type='release', si tu tapes "Apparat", Discogs renvoie les albums d'Apparat.

            # Si cela ne suffit pas, on peut retirer le paramètre type, mais il faudra filtrer plus bas.

            

            # TEST : On essaie sans filtre de type pour voir tout, et on triera nous-mêmes

            results = self.discogs.search(query)

            candidates = []

            count = 0

            total_items = 0

            

            # On itère sur les résultats

            for item in results:

                total_items += 1

                if count >= 10:

                    break

                # --- 1. FILTRAGE INTELLIGENT ---

                # On vérifie si c'est un album (Master/Release) en testant la présence d'attributs clés

                # Les Artist/Label n'ont généralement pas de 'title' ou 'artists' comme les albums

                # On utilise une approche permissive : si ça ressemble à un album, on le prend

                

                # Vérification : si l'objet n'a pas de titre, on le saute

                # (les Artist/Label n'ont généralement pas de title, mais les albums oui)

                if not hasattr(item, 'title') or not item.title:

                    continue

                # --- 2. EXTRACTION SÉCURISÉE (Airbag) ---

                try:

                    # Titre

                    title = item.title # Souvent "Artist - Album"

                    

                    # Artiste (Extraction propre)

                    artist = "Artiste Divers"

                    if hasattr(item, 'artists') and item.artists:

                        artist = item.artists[0].name

                    

                    # Si le titre contient déjà l'artiste (format Discogs classique "Artist - Title")

                    # On peut nettoyer pour l'affichage si besoin, mais gardons brut pour l'instant

                    

                    # Année

                    year = ""

                    if hasattr(item, 'year'):

                        year = str(item.year)

                    

                    # Label

                    label = ""

                    if hasattr(item, 'labels') and item.labels:

                        label = item.labels[0].name

                        

                    # Image (Thumb) - Gère tous les cas de figure

                    thumb = ""

                    if hasattr(item, 'thumb'):

                        thumb = item.thumb

                    elif hasattr(item, 'images') and item.images:

                        thumb = item.images[0].get('uri', '')

                    

                    # ID

                    discogs_id = item.id

                    candidates.append({

                        "discogs_id": discogs_id,

                        "title": title,

                        "artist": artist,

                        "year": year,

                        "label": label,

                        "thumb": thumb

                    })

                    count += 1

                    

                except Exception as item_error:

                    # Si UN élément est mal formé, on l'affiche dans la console mais on ne plante pas la liste

                    print(f"⚠️ Élément ignoré (Erreur de donnée) : {item_error}")

                    continue

            print(f"✅ {len(candidates)} résultats trouvés sur {total_items} éléments examinés pour '{query}'")

            return candidates

        except Exception as e:

            print(f"❌ Erreur critique recherche globale : {e}")

            return []



    def process_by_id(self, discogs_id):

        """Ajoute un album via son ID Discogs précis (Sélection utilisateur)"""

        print(f"💿 Récupération ID Discogs : {discogs_id}")

        try:

            # 1. On récupère l'objet précis via l'ID

            album = self.discogs.release(discogs_id)

            

            # Extraction des données (similaire au scan)

            artist_name = album.artists[0].name if album.artists else "Inconnu"

            if album.artists and len(album.artists) > 1:

                artist_name = ", ".join([a.name for a in album.artists])

            # 2. Spotify (On utilise les infos précises de Discogs)

            spotify_data = self.step_3_spotify(artist_name, album.title)

            

            # 3. Construction objet final

            final_cover = album.images[0]['uri'] if album.images else None

            spotify_link = None

            spotify_uri = None

            

            if spotify_data:

                spotify_link = spotify_data['spotify_link']

                spotify_uri = spotify_data['spotify_uri']

                if spotify_data['cover_hd']:

                    final_cover = spotify_data['cover_hd']

            clean_tracklist = [t.title for t in album.tracklist if t.position]

            return {

                "status": "success",

                "display": {

                    "artist": artist_name,

                    "title": album.title,

                    "cover_image": final_cover,

                },

                "details": {

                    "year": str(album.year) if album.year else "",

                    "label": album.labels[0].name if album.labels else "",

                    "genre": album.genres,

                    "tracklist": clean_tracklist

                },

                "links": {

                    "spotify_url": spotify_link,

                    "spotify_uri": spotify_uri,

                    "discogs_url": album.url

                }

            }

        except Exception as e:

            print(f"Erreur process ID: {e}")

            return {"status": "error", "message": str(e)}



# --- EXECUTION DE TEST ---

if __name__ == "__main__":

    # Instanciation

    app = KissaCore()

    

    # Image de test (Assure-toi d'avoir ce fichier dans le dossier)

    TEST_IMAGE = "test_vinyl.jpg" 

    

    if os.path.exists(TEST_IMAGE):

        print("🚀 Démarrage du crash test Kissa...")

        result = app.process(TEST_IMAGE)

        

        print("\n--- RÉSULTAT JSON FINAL ---")

        print(json.dumps(result, indent=4, ensure_ascii=False))

    else:

        print(f"❌ Fichier '{TEST_IMAGE}' introuvable. Ajoute une photo pour tester.")

