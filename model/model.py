import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load dataset
DATA_PATH = os.path.join(BASE_DIR, "data", "boq_train.csv")
data = pd.read_csv(DATA_PATH)

# Features and target
X = data[["cement_cum", "steel_mt", "brickwork_cum", "sand_cum", "labor_cost"]]
y = data["total_cost"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)

print("Model MAE:", mae)

# Save model
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
joblib.dump(model, MODEL_PATH)

print("Model saved at:", MODEL_PATH)
