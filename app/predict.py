import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

model = joblib.load(MODEL_PATH)
print("Model loaded successfully")

sample_boq = np.array([[  
    500,   # cement
    2.5,   # steel
    1200,  # bricks
    1800  # sq ft
]])

prediction = model.predict(sample_boq)
print("Predicted project cost:", prediction[0])
