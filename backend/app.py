from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)

# -------------------------
# ENABLE CORS (IMPORTANT)
# -------------------------
CORS(app, resources={r"/*": {"origins": "*"}})

# -------------------------
# PATH SETUP
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model_path = os.path.join(BASE_DIR, "models")
data_path = os.path.join(BASE_DIR, "data")

# -------------------------
# LOAD MODELS + COLUMNS
# -------------------------
model = joblib.load(os.path.join(model_path, "predict.pkl"))
clf = joblib.load(os.path.join(model_path, "classify.pkl"))
columns = joblib.load(os.path.join(model_path, "columns.pkl"))

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(os.path.join(data_path, "Metro_Interstate_Traffic_Volume.csv"))

df['date_time'] = pd.to_datetime(df['date_time'])
df['hour'] = df['date_time'].dt.hour
df['day_of_week'] = df['date_time'].dt.dayofweek
df['month'] = df['date_time'].dt.month


# -------------------------
# HELPER FUNCTION
# -------------------------
def prepare_input(data):
    input_df = pd.DataFrame([data])

    # Add missing columns
    for col in columns:
        if col not in input_df:
            input_df[col] = 0

    # Ensure correct order
    input_df = input_df[columns]

    return input_df


# -------------------------
# 1. GET DATA
# -------------------------
@app.route('/get-data', methods=['GET'])
def get_data():
    return df.head(200).to_json(orient='records')


# -------------------------
# 2. PREDICT
# -------------------------
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    input_df = prepare_input(data)
    prediction = model.predict(input_df)[0]

    return jsonify({"prediction": int(prediction)})


# -------------------------
# 3. CLASSIFY
# -------------------------
@app.route('/classify', methods=['POST'])
def classify():
    data = request.json

    input_df = prepare_input(data)
    result = clf.predict(input_df)[0]

    levels = ["Low", "Medium", "High"]

    return jsonify({"traffic_level": levels[result]})


# -------------------------
# 4. INSIGHTS
# -------------------------
@app.route('/insights', methods=['GET'])
def insights():
    peak_hour = df.groupby('hour')['traffic_volume'].mean().idxmax()
    avg_traffic = int(df['traffic_volume'].mean())

    return jsonify({
        "peak_hour": int(peak_hour),
        "average_traffic": avg_traffic
    })


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)