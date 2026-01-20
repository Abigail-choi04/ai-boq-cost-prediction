from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

model = joblib.load(MODEL_PATH)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    X = np.array([[
        data["cement_cum"],
        data["steel_mt"],
        data["brickwork_cum"],
        data["sand_cum"],
        data["labor_cost"]
    ]])

    cost = model.predict(X)[0]

    return jsonify({
        "predicted_cost": float(cost),
        "currency": "INR"
    })


if __name__ == "__main__":
    app.run(debug=True)
