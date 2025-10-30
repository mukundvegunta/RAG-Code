import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np

import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np

# Load data from GitHub
url = "https://github.com/akarshsinghh/Football-Player-Market-Value-Prediction/raw/main/Final3.xlsx"
df = pd.read_excel(url)

# Use 'MV' for market value, drop irrelevant columns
exclude_columns = ['MV', 'Player', 'Nation', 'Pos', 'Club', 'Leauge']
X = df.drop(exclude_columns, axis=1, errors='ignore').select_dtypes(include=[np.number])
y = df['MV']

# Train/test split and scaling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Lasso regression with cross-validation
lasso = LassoCV(cv=5, random_state=42)
lasso.fit(X_train_scaled, y_train)

# Output coefficients, lambda, and test R^2 score
print("Lasso coefficients:")
print(dict(zip(X.columns, lasso.coef_)))
print("Test set R^2 score:", lasso.score(X_test_scaled, y_test))
print("Chosen lambda (alpha):", lasso.alpha_)

