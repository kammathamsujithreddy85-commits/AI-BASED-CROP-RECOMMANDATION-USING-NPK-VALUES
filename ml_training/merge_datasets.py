import pandas as pd
import numpy as np
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'Crop_recommendation.csv')

# Load your existing dataset
df = pd.read_csv(csv_path)
print(f"Original dataset: {len(df)} records")

def augment_dataset(df, n_samples_per_crop=100):
    """Add realistic variations to existing data"""
    augmented_rows = []
    
    for crop in df['label'].unique():
        crop_data = df[df['label'] == crop]
        
        for _ in range(n_samples_per_crop):
            new_row = {
                'N': np.clip(crop_data['N'].mean() * np.random.uniform(0.95, 1.05), 0, 200),
                'P': np.clip(crop_data['P'].mean() * np.random.uniform(0.95, 1.05), 0, 150),
                'K': np.clip(crop_data['K'].mean() * np.random.uniform(0.95, 1.05), 0, 250),
                'temperature': np.clip(crop_data['temperature'].mean() * np.random.uniform(0.95, 1.05), 0, 50),
                'humidity': np.clip(crop_data['humidity'].mean() * np.random.uniform(0.95, 1.05), 0, 100),
                'ph': np.clip(crop_data['ph'].mean() * np.random.uniform(0.95, 1.05), 0, 14),
                'rainfall': np.clip(crop_data['rainfall'].mean() * np.random.uniform(0.95, 1.05), 0, 300),
                'label': crop
            }
            augmented_rows.append(new_row)
    
    return pd.DataFrame(augmented_rows)

# Create augmented dataset
df_augmented = augment_dataset(df, n_samples_per_crop=150)
df_combined = pd.concat([df, df_augmented], ignore_index=True)
df_combined = df_combined.drop_duplicates()

print(f"Augmented dataset: {len(df_combined)} records")
print(f"Crops: {df_combined['label'].nunique()}")

# Save
output_path = os.path.join(script_dir, 'Crop_recommendation_augmented.csv')
df_combined.to_csv(output_path, index=False)
print(f"✅ Saved to: {output_path}")