from flask import Flask, request, render_template
import pickle
import os
import numpy as np

app = Flask(__name__)
Atharva patil
# Load model
model_path = 'fraud_model.pkl'

if not os.path.exists(model_path):
    raise FileNotFoundError("❌ model.pkl NOT FOUND! Put it in same folder")

model = pickle.load(open(model_path, 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Input features (8 + 2 dummy)
        features = [[
            float(request.form['step']),
            float(request.form['type']),
            float(request.form['amount']),
            float(request.form['oldbalanceOrg']),
            float(request.form['newbalanceOrig']),
            float(request.form['oldbalanceDest']),
            float(request.form['newbalanceDest']),
            float(request.form['isFlaggedFraud']),
            0,   # dummy
            0    # dummy
        ]]

        features = np.array(features)

        # 🔥 Get fraud probability
        prob = model.predict_proba(features)[0][1]

        # 🔥 DEBUG (check in terminal)
        print("Fraud Probability:", prob)

        # 🔥 VERY LOW threshold (guaranteed fraud detection)
        if prob > 0.01:
            result = "⚠️ Fraud Transaction"
        else:
            result = "✅ Legit Transaction"

        return render_template(
            'index.html',
            prediction_text=result,
            probability=round(prob * 100, 2)
        )

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
