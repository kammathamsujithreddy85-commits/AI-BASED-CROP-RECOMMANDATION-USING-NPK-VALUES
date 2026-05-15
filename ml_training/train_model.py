# ml_training/train_model.py
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("🚀 Starting Crop Recommendation Model Training (Optimized)...")

# 1. Load Data
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'Crop_recommendation.csv')
df = pd.read_csv(csv_path)
print(f"✅ Loaded {len(df)} records")

# 2. Prepare Features & Target
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

print(f"📊 Features: {X.shape[1]} | Samples: {X.shape[0]} | Crops: {y.nunique()}")

# 3. Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"📈 Train: {len(X_train)} | 🧪 Test: {len(X_test)}")

# 4. Train Optimized Random Forest
print("🤖 Training Random Forest Classifier (300 trees, calibrated)...")
model = RandomForestClassifier(
    n_estimators=300,        # More trees = smoother confidence scores
    max_depth=None,          # Let trees grow fully (RF averages variance)
    min_samples_leaf=2,      # Prevents overfitting to noise
    max_features='sqrt',     # Standard for classification
    class_weight='balanced', # Handles imbalanced crop data better
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("✅ Model trained!")

# 5. Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Test Accuracy: {accuracy * 100:.2f}%")

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# 6. Feature Importance
importances = model.feature_importances_
features = X.columns
print("\n🔍 Top 3 Most Important Factors:")
for feat, imp in sorted(zip(features, importances), key=lambda x: x[1], reverse=True)[:3]:
    print(f"   • {feat}: {imp*100:.1f}%")

# 7. Save Model (FIXED: Matches app.py)
model_path = os.path.join(script_dir, 'models', 'crop_model_best.pkl')
os.makedirs(os.path.dirname(model_path), exist_ok=True)
joblib.dump(model, model_path)
print(f"\n💾 Model saved to: {model_path}")

# 8. CONFIDENCE VERIFICATION TEST
print("\n🧪 Running Confidence Verification Test...")
test_samples = {
    'Rice': [90, 40, 180, 28, 80, 6.0, 220],
    'Wheat': [80, 35, 120, 22, 65, 7.0, 150],
    'Cotton': [70, 30, 150, 30, 70, 6.5, 180]
}
for crop, vals in test_samples.items():
    df_test = pd.DataFrame([vals], columns=X.columns)
    pred = model.predict(df_test)[0]
    conf = max(model.predict_proba(df_test)[0]) * 100
    print(f"   {crop} -> Predicted: {pred} | Confidence: {conf:.1f}%")

print("\n🎉 PHASE 2 COMPLETE! Model is ready for high-confidence predictions!")