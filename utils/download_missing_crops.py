import requests
import os

missing_crops = {
    'kidneybeans': 'https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=600',
    'pigeonpea': 'https://images.unsplash.com/photo-1615486511484-92e172cc4fe0?w=600',
    'moong': 'https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=600',
    'mothbeans': 'https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=600',
    'urad': 'https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?w=600',
    'oilseeds': 'https://images.unsplash.com/photo-1628151015976-9f1ffc700c55?w=600',
    'mustard': 'https://images.unsplash.com/photo-1485594050905-1ae94d8287ad?w=600',
    'jowar': 'https://images.unsplash.com/photo-1628151015976-9f1ffc700c55?w=600',
    'bajra': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600',
    'ragi': 'https://images.unsplash.com/photo-1586771107445-d3ca158fd433?w=600'
}

os.makedirs('static/images/crop', exist_ok=True) 

for crop, url in missing_crops.items():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filepath = f"static/images/crop/{crop}.jpg"
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {crop}")
        else:
            print(f"Failed: {crop}")
    except Exception as e:
        print(f"Error {crop}: {e}")

print("\nDownload complete!")
