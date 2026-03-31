import requests
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')

def fetch_pexels_wallpapers(query="nature", per_page=20, page=1):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page={per_page}&page={page}"
    headers = {"Authorization": PEXELS_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('photos', [])
    except:
        pass
    return []

def get_curated_wallpapers(per_page=20):
    url = f"https://api.pexels.com/v1/curated?per_page={per_page}"
    headers = {"Authorization": PEXELS_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('photos', [])
    except:
        pass
    return []
