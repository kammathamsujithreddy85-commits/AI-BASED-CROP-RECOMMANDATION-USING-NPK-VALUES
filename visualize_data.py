import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
df = pd.read_csv("ml_training/Crop_recommendation.csv")

# Create plots folder
os.makedirs("visualizations", exist_ok=True)

# Plot 1: Correlation Heatmap
plt.figure(figsize=(10, 8))
numeric_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
corr_matrix = df[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Feature Correlation Matrix')
plt.tight_layout()
plt.savefig('visualizations/correlation_heatmap.png', dpi=300)
plt.close()
print("✓ Saved: correlation_heatmap.png")

# Plot 2: Crop Distribution (confirm balance)
plt.figure(figsize=(12, 6))
df['label'].value_counts().plot(kind='bar', color='steelblue')
plt.title('Sample Distribution per Crop (22 crops × 100 samples)')
plt.xlabel('Crop Type')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('visualizations/crop_distribution.png', dpi=300)
plt.close()
print("✓ Saved: crop_distribution.png")

# Plot 3: NPK ranges by crop category
plt.figure(figsize=(14, 6))
df_melted = df.melt(id_vars=['label'], value_vars=['N', 'P', 'K'], 
                    var_name='Nutrient', value_name='Value')
sns.boxplot(data=df_melted, x='label', y='Value', hue='Nutrient')
plt.title('NPK Distribution Across Crops')
plt.xlabel('Crop Type')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('visualizations/npk_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: npk_boxplot.png")

print("\n✅ All visualizations complete! Check the 'visualizations' folder.")