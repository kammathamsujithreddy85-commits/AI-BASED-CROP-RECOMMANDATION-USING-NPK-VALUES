import requests
import os

CROP_IMAGES = {
    'rice': 'https://images.unsplash.com/photo-1586771107445-d3ca158fd433?w=600',
    'wheat': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600',
    'maize': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=600',
    'cotton': 'https://images.unsplash.com/photo-1599571274496-964528e0fd6f?w=600',
    'sugarcane': 'https://images.unsplash.com/photo-1605000797499-25d4b5661978?w=600',
    'potato': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=600',
    'onion': 'https://images.unsplash.com/photo-1618512496228-09768512d1eb?w=600',
    'tomato': 'https://images.unsplash.com/photo-1592924357228-91a4daadc42a?w=600',
    'groundnut': 'https://images.unsplash.com/photo-1628151015976-9f1ffc700c55?w=600',
    'soybean': 'https://images.unsplash.com/photo-1589923121172-b8a958f50621?w=600',
    'mustard': 'https://images.unsplash.com/photo-1485594050905-1ae94d8287ad?w=600',
    'chickpea': 'https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=600',
    'pigeonpea': 'https://images.unsplash.com/photo-1615486511484-92e172cc4fe0?w=600',
    'moong': 'https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=600',
    'urad': 'https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=600',
    'barley': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600',
    'jowar': 'https://images.unsplash.com/photo-1628151015976-9f1ffc700c55?w=600',
    'bajra': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600',
    'ragi': 'https://images.unsplash.com/photo-1586771107445-d3ca158fd433?w=600',
    'sunflower': 'https://images.unsplash.com/photo-1496568816309-51d7c20e3b21?w=600',
    'sesame': 'https://images.unsplash.com/photo-1628151015976-9f1ffc700c55?w=600',
    'castor': 'https://images.unsplash.com/photo-1628151015976-9f1ffc700c55?w=600',
    'kidneybeans': 'https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=600',
    'mothbeans': 'https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=600',
    'oilseeds': 'https://images.unsplash.com/photo-1628151015976-9f1ffc700c55?w=600'
}

os.makedirs('static/images/crop', exist_ok=True)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("Starting download of all crop images...")
for crop, url in CROP_IMAGES.items():
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Check if it's a valid image (not a tiny text file)
            if len(response.content) > 1000:
                filepath = f"static/images/crop/{crop}.jpg"
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {crop}")
            else:
                print(f"Failed (Invalid Image): {crop}")
        else:
            print(f"Failed (HTTP {response.status_code}): {crop}")
    except Exception as e:
        print(f"Error {crop}: {e}")

print("Download complete!")
