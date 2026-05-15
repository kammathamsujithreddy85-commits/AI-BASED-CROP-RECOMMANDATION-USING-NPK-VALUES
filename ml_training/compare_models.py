# ml_training/compare_models.py
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import time

print("="*70)
print("🔬 MULTI-MODEL COMPARISON FOR CROP RECOMMENDATION")
print("="*70)

# 1. Load Data
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'Crop_recommendation.csv')
df = pd.read_csv(csv_path)
print(f"\n✅ Loaded {len(df)} records")

# 2. Prepare Features & Target
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# 3. Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"📈 Train: {len(X_train)} | 🧪 Test: {len(X_test)}")

# 4. Scale Data (Needed for SVM, KNN, Logistic Regression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Define 5 Models
# 5. Define 5 Models
models = {
    'Random Forest': {
        'model': RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1),
        'train_data': (X_train, y_train),
        'test_data': (X_test, y_test),
        'scale': False
    },
    'Decision Tree': {
        'model': DecisionTreeClassifier(max_depth=15, random_state=42),
        'train_data': (X_train, y_train),
        'test_data': (X_test, y_test),
        'scale': False
    },
    'SVM': {
        'model': SVC(kernel='rbf', C=10, gamma='scale', random_state=42),
        'train_data': (X_train_scaled, y_train),
        'test_data': (X_test_scaled, y_test),
        'scale': True
    },
    'KNN': {
        'model': KNeighborsClassifier(n_neighbors=5, weights='distance', n_jobs=-1),
        'train_data': (X_train_scaled, y_train),
        'test_data': (X_test_scaled, y_test),
        'scale': True
    },
    'Logistic Regression': {
        'model': LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1),
        'train_data': (X_train_scaled, y_train),
        'test_data': (X_test_scaled, y_test),
        'scale': True
    }
}
# 6. Train and Evaluate All Models
results = []

print("\n" + "="*70)
print("🤖 TRAINING & EVALUATING MODELS")
print("="*70)

for name, config in models.items():
    print(f"\n⏳ Training {name}...")
    start_time = time.time()
    
    model = config['model']
    X_tr, y_tr = config['train_data']
    model.fit(X_tr, y_tr)
    
    X_te, y_te = config['test_data']
    y_pred = model.predict(X_te)
    
    train_time = time.time() - start_time
    accuracy = accuracy_score(y_te, y_pred) * 100
    
    results.append({
        'Model': name,
        'Accuracy (%)': accuracy,
        'Training Time (s)': round(train_time, 2)
    })
    
    print(f"✅ {name}: {accuracy:.2f}% accuracy (Time: {train_time:.2f}s)")

# 7. Create Results Table
results_df = pd.DataFrame(results)
results_df = results_df.sort_values('Accuracy (%)', ascending=False)

print("\n" + "="*70)
print("📊 MODEL COMPARISON RESULTS")
print("="*70)
print(results_df.to_string(index=False))

# 8. Save Best Model
best_model_name = results_df.iloc[0]['Model']
best_accuracy = results_df.iloc[0]['Accuracy (%)']

print(f"\n🏆 BEST MODEL: {best_model_name} with {best_accuracy:.2f}% accuracy")

# Save the best model
if best_model_name == 'Random Forest':
    best_model = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
    best_model.fit(X_train, y_train)
elif best_model_name == 'Decision Tree':
    best_model = DecisionTreeClassifier(max_depth=15, random_state=42)
    best_model.fit(X_train, y_train)
elif best_model_name == 'SVM':
    best_model = SVC(kernel='rbf', C=10, gamma='scale', random_state=42)
    best_model.fit(X_train_scaled, y_train)

model_path = os.path.join(script_dir, 'models', 'crop_model_best.pkl')
joblib.dump(best_model, model_path)
print(f"💾 Best model saved to: {model_path}")

# Save comparison results
results_path = os.path.join(script_dir, 'models', 'model_comparison.csv')
results_df.to_csv(results_path, index=False)
print(f"💾 Comparison saved to: {results_path}")

# 9. Create Chart
print("\n📈 Creating visualization...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Chart 1: Accuracy
axes[0].barh(results_df['Model'], results_df['Accuracy (%)'], 
             color=['#667eea', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'])
axes[0].set_xlabel('Accuracy (%)')
axes[0].set_title('🎯 Model Accuracy Comparison')
axes[0].grid(axis='x', alpha=0.3)

# Chart 2: Training Time
axes[1].bar(results_df['Model'], results_df['Training Time (s)'],
            color=['#667eea', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'])
axes[1].set_ylabel('Time (seconds)')
axes[1].set_title('⏱️ Training Time Comparison')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plot_path = os.path.join(script_dir, 'models', 'model_comparison.png')
plt.savefig(plot_path, dpi=300, bbox_inches='tight')
print(f"💾 Chart saved to: {plot_path}")

print("\n" + "="*70)
print("✅ MODEL COMPARISON COMPLETE!")
print("="*70)