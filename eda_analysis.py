import pandas as pd

df = pd.read_csv("ml_training/Crop_recommendation.csv")
print(df.info())
print("\n" + "="*50 + "\n")
print(df.describe())
print("\n" + "="*50 + "\n")
print(df["label"].value_counts())