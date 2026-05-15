import pandas as pd
import joblib

# Load data and model
df = pd.read_csv('ml_training/Crop_recommendation.csv')
model = joblib.load('ml_training/models/crop_model_best.pkl')

# Find sample values for common crops
crops_to_test = ['rice', 'wheat', 'cotton', 'coconut', 'coffee']

print("🔍 Testing ACTUAL values from your dataset:\n")

for crop in crops_to_test:
    # Get 3 random samples of this crop from the dataset
    samples = df[df['label'] == crop].sample(min(3, len(df[df['label'] == crop])))
    
    for idx, row in samples.iterrows():
        test_input = pd.DataFrame([[
            row['N'], row['P'], row['K'], 
            row['temperature'], row['humidity'], 
            row['ph'], row['rainfall']
        ]], columns=['N','P','K','temperature','humidity','ph','rainfall'])
        
        pred = model.predict(test_input)[0]
        conf = max(model.predict_proba(test_input)[0]) * 100
        
        print(f"{crop.upper()}:")
        print(f"  N={row['N']}, P={row['P']}, K={row['K']}")
        print(f"  Temp={row['temperature']}, Hum={row['humidity']}, pH={row['ph']}, Rain={row['rainfall']}")
        print(f"  → Predicted: {pred} | Confidence: {conf:.1f}%\n")