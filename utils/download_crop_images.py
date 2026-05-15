import os
import requests
import time

CROPS = [
    'rice', 'wheat', 'maize', 'chickpea', 'kidneybeans', 'pigeonpea',
    'moong', 'mothbeans', 'urad', 'cotton', 'oilseeds', 'sugarcane',
    'potato', 'onion', 'tomato', 'groundnut', 'soybean', 'mustard',
    'jowar', 'bajra', 'barley', 'ragi'
]

# We will use Unsplash Source API (source.unsplash.com is deprecated but redirected to normal unsplash or we can use regular unsplash search API if we had a key).
# Alternatively, Wikimedia Commons or Pixabay (if we have a key).
# Given we don't have an API key here, we'll try to download from Wikimedia Commons API, which is free and doesn't require a key.

def download_images(output_dir="static/images/crops"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting download for {len(CROPS)} crops...")
    
    for crop in CROPS:
        file_path = os.path.join(output_dir, f"{crop}.jpg")
        if os.path.exists(file_path):
            print(f"[{crop}] Already exists. Skipping.")
            continue
            
        print(f"[{crop}] Fetching image...")
        
        # Using Wikimedia Commons API
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={crop}%20(crop)|{crop}"
        headers = {'User-Agent': 'CropAI/1.0 (Contact: admin@example.com)'}
        
        try:
            response = requests.get(search_url, headers=headers).json()
            pages = response.get("query", {}).get("pages", {})
            
            image_url = None
            for page_id, page_data in pages.items():
                if "original" in page_data:
                    image_url = page_data["original"]["source"]
                    break
                    
            if image_url:
                img_data = requests.get(image_url, headers=headers).content
                with open(file_path, 'wb') as handler:
                    handler.write(img_data)
                print(f"[{crop}] ✅ Successfully downloaded")
            else:
                print(f"[{crop}] ❌ No image found on Wikipedia")
                
        except Exception as e:
            print(f"[{crop}] ⚠️ Error: {str(e)}")
            
        # Be nice to APIs
        time.sleep(1)
        
    print("Download complete!")

if __name__ == "__main__":
    download_images()
