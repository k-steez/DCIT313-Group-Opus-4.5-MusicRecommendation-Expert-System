import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

cid = os.getenv("SPOTIPY_CLIENT_ID") or os.getenv("CLIENT_ID")
secret = os.getenv("SPOTIPY_CLIENT_SECRET") or os.getenv("CLIENT_SECRET")
print("CID present:", bool(cid), "SECRET present:", bool(secret))

try:
    auth = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    token_info = auth.get_access_token(as_dict=True)
    print("Token info:", token_info)
except Exception as e:
    print("ERROR getting token:", repr(e))
    raise

try:
    sp = spotipy.Spotify(auth=token_info["access_token"])
    features = sp.audio_features(["7qiZfU4dY1lWllzX7mPBI3"])
    print("Features:", features)
except Exception as e:
    print("ERROR calling audio_features:", repr(e))
    raise