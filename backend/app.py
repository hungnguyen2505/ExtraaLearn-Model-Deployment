
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load trained model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "extraalearn_pipeline.joblib"
)

model = joblib.load(MODEL_PATH)

# Features required for prediction
FEATURES = [
    "age",
    "current_occupation",
    "first_interaction",
    "profile_completed",
    "website_visits",
    "time_spent_on_website",
    "page_views_per_visit",
    "last_activity",
    "print_media_type1",
    "print_media_type2",
    "digital_media",
    "educational_channels",
    "referral"
]

NUMERICAL_FEATURES = [
    "age",
    "website_visits",
    "time_spent_on_website",
    "page_views_per_visit"
]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "A JSON object is required"
            }), 400

        missing = [f for f in FEATURES if f not in data]

        if missing:
            return jsonify({
                "error": "Missing features",
                "missing": missing
            }), 400

        input_df = pd.DataFrame([data])[FEATURES]

        for col in NUMERICAL_FEATURES:
            input_df[col] = pd.to_numeric(
                input_df[col], errors="raise"
            )

        prediction = int(model.predict(input_df)[0])

        probability = float(
            model.predict_proba(input_df)[0][1]
        )

        return jsonify({
            "prediction": prediction,
            "conversion_probability": round(probability, 4)
        })

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed"
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
