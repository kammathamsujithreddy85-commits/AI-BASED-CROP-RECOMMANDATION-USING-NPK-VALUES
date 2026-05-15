# ml_training/test_data.py
import pandas as pd
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the full path to the CSV file
csv_path = os.path.join(script_dir, 'Crop_recommendation.csv')

print(f"📂 Looking for file at: {csv_path}")

# Check if file exists before loading
if os.path.exists(csv_path):
    print("✅ File found! Loading dataset...\n")
    
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # Display information
    print("✅ Dataset loaded successfully!")
    print(f"\n📊 Shape: {df.shape}")
    print(f"\n📋 Columns: {df.columns.tolist()}")
    print(f"\n🌾 Unique crops: {df['label'].nunique()}")
    print(f"\n📝 First 5 rows:")
    print(df.head())
    print(f"\n📈 Data types:")
    print(df.dtypes)
    print(f"\n❓ Missing values:")
    print(df.isnull().sum())
else:
    print("❌ ERROR: File not found!")
    print(f"   Expected at: {csv_path}")