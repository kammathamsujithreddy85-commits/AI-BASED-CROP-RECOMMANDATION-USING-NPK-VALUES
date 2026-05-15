import requests
import os
import time
import json

CROPS = [
    'rice', 'wheat', 'maize', 'chickpea', 'kidneybeans', 'pigeonpea',
    'moong', 'mothbeans', 'urad', 'cotton', 'oilseeds', 'sugarcane',
    'potato', 'onion', 'tomato', 'groundnut', 'soybean', 'mustard',
    'jowar', 'bajra', 'barley', 'ragi'
]

SEARCH_TERMS = {
    'moong': 'mung bean',
    'urad': 'Vigna mungo',
    'jowar': 'Sorghum bicolor',
    'bajra': 'Pearl millet',
    'ragi': 'Eleusine coracana',
    'mothbeans': 'Vigna aconitifolia',
    'oilseeds': 'Oilseed',
    'kidneybeans': 'Kidney bean',
    'groundnut': 'Peanut',
    'chickpea': 'Chickpea'
}

def get_wikimedia_image(crop_name):
    search_term = SEARCH_TERMS.get(crop_name, crop_name)
    
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={search_term}"
    headers = {'User-Agent': 'CropAIDownloader/1.0 (Student Project)'}
    
    try:
        response = requests.get(search_url, headers=headers).json()
        pages = response.get('query', {}).get('pages', {})
        
        for page_id, page_data in pages.items():
            if 'original' in page_data:
                return page_data['original']['source']
                
        commons_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrsearch={search_term}%20crop&gsrlimit=1&prop=imageinfo&iiprop=url&format=json"
        response = requests.get(commons_url, headers=headers).json()
        pages = response.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'imageinfo' in page_data:
                return page_data['imageinfo'][0]['url']
                
    except Exception as e:
        print(f"  Error fetching API for {crop_name}: {e}")
    return None

def download_all():
    os.makedirs('static/images/crop', exist_ok=True)
    headers = {'User-Agent': 'CropAIDownloader/1.0'}
    
    print("Starting reliable image download from Wikimedia Commons...")
    for crop in CROPS:
        filepath = f"static/images/crop/{crop}.jpg"
        
        if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
            print(f"[{crop}] Already exists and is valid.")
            continue
            
        print(f"[{crop}] Searching for image...")
        img_url = get_wikimedia_image(crop)
        
        if img_url:
            try:
                img_data = requests.get(img_url, headers=headers).content
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                print(f"[{crop}] Downloaded successfully from Wikipedia.")
            except Exception as e:
                print(f"[{crop}] Failed to download file: {e}")
        else:
            print(f"[{crop}] No image found.")
            
        time.sleep(1)

if __name__ == "__main__":
    download_all()
