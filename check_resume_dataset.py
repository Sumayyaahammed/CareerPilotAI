import pandas as pd

# Load the dataset
df = pd.read_csv("data/resumes/Resume.csv")

print("First 5 rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nResume Categories:")
print(df["Category"].value_counts())