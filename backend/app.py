from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# -------------------------
# PATH SETUP
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model_path = os.path.join(BASE_DIR, "models")
data_path = os.path.join(BASE_DIR, "data")

# -------------------------
# LOAD MODELS
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
# MONGODB CONNECTION
# -------------------------
client = MongoClient("mongodb://mongo:27017/")
db = client["traffic_db"]
collection = db["predictions"]

# -------------------------
# HELPER FUNCTION
# -------------------------
def prepare_input(data):
    input_df = pd.DataFrame([data])

    # Handle categorical manually if needed
    if 'weather_main' in input_df:
        input_df = pd.get_dummies(input_df)

    # Ensure all columns exist
    for col in columns:
        if col not in input_df:
            input_df[col] = 0

    input_df = input_df[columns]
    return input_df

# -------------------------
# ROUTES
# -------------------------

@app.route('/')
def home():
    return "Traffic Analysis Backend Running"

@app.route('/get-data', methods=['GET'])
def get_data():
    return df.head(200).to_json(orient='records')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        input_df = prepare_input(data)
        prediction = model.predict(input_df)[0]

        # STORE IN MONGO
        collection.insert_one({
            "input": data,
            "prediction": int(prediction)
        })

        return jsonify({
            "prediction": int(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/classify', methods=['POST'])
def classify():
    try:
        data = request.json

        input_df = prepare_input(data)
        result = clf.predict(input_df)[0]

        levels = ["Low", "Medium", "High"]

        return jsonify({
            "traffic_level": levels[result]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/insights', methods=['GET'])
def insights():
    peak_hour = df.groupby('hour')['traffic_volume'].mean().idxmax()
    avg_traffic = int(df['traffic_volume'].mean())

    return jsonify({
        "peak_hour": int(peak_hour),
        "average_traffic": avg_traffic
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)