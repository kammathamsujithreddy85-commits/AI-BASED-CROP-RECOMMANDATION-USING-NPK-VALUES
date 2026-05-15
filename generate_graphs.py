# Save this as 'generate_graphs.py' in your main folder
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('ml_training/Crop_recommendation.csv')

# 1. NPK Correlation Heatmap (Looks very professional for Data Science)
plt.figure(figsize=(8, 6))
sns.heatmap(df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].corr(), annot=True, cmap='coolwarm')
plt.title('Feature Correlation Heatmap')
plt.savefig('heatmap.png')
print("Saved heatmap.png")

# 2. NPK Distribution Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['N', 'P', 'K']])
plt.title('NPK Nutrient Distribution')
plt.savefig('npk_boxplot.png')
print("Saved npk_boxplot.png")

# 3. Crop Count (Show dataset balance)
plt.figure(figsize=(10, 5))
df['label'].value_counts().head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Crops in Dataset')
plt.savefig('crop_count.png')
print("Saved crop_count.png")