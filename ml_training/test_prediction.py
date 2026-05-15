import joblib
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(script_dir, 'models', 'crop_model.pkl'))

print("🌾 CROP RECOMMENDATION SYSTEM")
print("=" * 50)

# Test with sample data
sample_input = {
    'N': [90],
    'P': [42], 
    'K': [43],
    'temperature': [20.8],
    'humidity': [82.0],
    'ph': [6.5],
    'rainfall': [202.9]
}

import pandas as pd
df = pd.DataFrame(sample_input)
prediction = model.predict(df)[0]

print(f"\nInput: N=90, P=42, K=43, Temp=20.8°C")
print(f"       Humidity=82%, pH=6.5, Rainfall=202mm")
print(f"\n✅ Recommended Crop: {prediction.upper()}")
print("=" * 50)