# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Step 1: Load dataset from GitHub (link to CSV or XLSX)
url = "https://github.com/akarshsinghh/Football-Player-Market-Value-Prediction/raw/main/Final3.xlsx"
df = pd.read_excel(url)

# Step 2: Basic cleaning
df = df.dropna(subset=['MV'])
df = df.select_dtypes(include=[np.number])  # Keep only numeric columns

# Step 3: Correlation matrix
corr = df.corr()['MV'].sort_values(ascending=False)
print("Top correlated variables with MarketValue:")
print(corr.head(10))

# Step 4: Visualize correlation heatmap
plt.figure(figsize=(10,6))
sns.heatmap(df.corr(), cmap='coolwarm', center=0)
plt.title("Feature Correlation Heatmap")
plt.show()

# Step 5: Regression to assess feature importance
X = df.drop(columns=['MV'])
y = df['MV']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Step 6: Feature importance analysis
importances = pd.Series(model.feature_importances_, index=X.columns)
top_features = importances.sort_values(ascending=False)[:10]
print("Top 10 most influential features:")
print(top_features)

# Step 7: Visualize feature importance
top_features.plot(kind='bar', title='Top Features Influencing Market Value')
plt.show()

# Evaluate model
y_pred = model.predict(X_test)
print("R² Score:", r2_score(y_test, y_pred))

# 1. Distribution of market value (MV)
#plt.figure(figsize=(8,5))
#sns.histplot(y, bins=30, kde=True, color='skyblue')
#plt.title("Distribution of Player Market Value (MV)")
#plt.xlabel("Market Value")
#plt.ylabel("Frequency")
#plt.tight_layout()
#plt.show()

# 2. Age vs Market Value Scatterplot
#if 'Age' in df.columns:
    #plt.figure(figsize=(8,5))
    #sns.boxplot(data=df, x='Age', y='MV', color='orange')
    #plt.title("Age vs Market Value")
    #plt.xlabel("Age")
    #plt.ylabel("Market Value (MV)")
    #plt.tight_layout()
    #plt.show()

# 3. Market Value by Position 
#if 'Pos' in df.columns:
    #plt.figure(figsize=(10,6))
    #sns.boxplot(data=df, x='Pos', y='MV', palette='Set2')
    #plt.title('Market Value by Player Position')
    #plt.xlabel('Player Position (Pos)')
    #plt.ylabel('Market Value (MV)')
    #plt.xticks(rotation=45)
    #plt.tight_layout()
    #plt.show()

