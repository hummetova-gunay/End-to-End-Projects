from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import joblib
import os

# Create dummy dataset
X, y = make_regression(n_samples=100, n_features=3, noise=0.1)

# Train model
model = LinearRegression()
model.fit(X, y)

# Create model directory if not exists
os.makedirs("model", exist_ok=True)

# Save model
joblib.dump(model, "model/model.joblib")

print("Model saved!")
