import joblib
import matplotlib.pyplot as plt
import numpy as np

# Load model
model = joblib.load('ml_training/models/crop_model_best.pkl')

# Feature names
features = ['N', 'P', 'K', 'Temperature', 'Humidity', 'pH', 'Rainfall']

# Get feature importances
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

# Plot
plt.figure(figsize=(10, 6))
plt.title('Feature Importance - Random Forest Model', fontsize=14, fontweight='bold')
plt.barh(range(len(features)), [importances[i] for i in indices], color='#2E86AB', edgecolor='black')
plt.yticks(range(len(features)), [features[i] for i in indices], fontsize=11)
plt.xlabel('Importance Score', fontsize=12)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Feature importance saved as 'feature_importance.png'")