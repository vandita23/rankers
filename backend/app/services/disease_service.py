"""Crop disease detection service using Roboflow."""

from io import BytesIO

from PIL import Image
from inference_sdk import InferenceHTTPClient

from app.core.config import ROBOFLOW_API_KEY


CONFIDENCE_THRESHOLD = 70

ROBOFLOW_API_URL = "https://serverless.roboflow.com"
ROBOFLOW_MODEL_ID = "plant-and-disease-identification/7"


if not ROBOFLOW_API_KEY:
    raise RuntimeError("ROBOFLOW_API_KEY is not configured.")


_client = InferenceHTTPClient(
    api_url=ROBOFLOW_API_URL,
    api_key=ROBOFLOW_API_KEY,
)


def _get_actions(disease: str, language: str) -> list[str]:
    """Return simple farmer-friendly actions based on the prediction."""

    disease_lower = disease.lower()

    if "healthy" in disease_lower:
        if language == "hi":
            return [
                "पौधे की नियमित निगरानी करते रहें",
                "सिंचाई और पोषण की उचित मात्रा बनाए रखें",
                "आसपास के पौधों में बीमारी के लक्षणों पर नज़र रखें",
            ]

        return [
            "Continue monitoring the crop regularly",
            "Maintain appropriate irrigation and nutrition",
            "Watch nearby plants for signs of disease",
        ]

    if language == "hi":
        return [
            "प्रभावित पौधे को अन्य पौधों से अलग रखें",
            "आसपास के पौधों में बीमारी के लक्षणों की जांच करें",
            "उपचार के लिए स्थानीय कृषि विशेषज्ञ की सलाह लें",
        ]

    return [
        "Separate affected plants where practical",
        "Check nearby plants for similar symptoms",
        "Consult a local agricultural expert for treatment advice",
    ]


def _extract_prediction(result: dict) -> tuple[str | None, float]:
    """Extract the highest-confidence prediction from Roboflow's response."""

    predictions = result.get("predictions", [])

    if not predictions:
        return None, 0.0

    best_prediction = max(
        predictions,
        key=lambda prediction: float(
            prediction.get("confidence", 0)
        ),
    )

    disease = (
        best_prediction.get("class")
        or best_prediction.get("class_name")
    )

    confidence = float(
        best_prediction.get("confidence", 0)
    )

    return disease, confidence


def _translate_disease(disease: str, language: str) -> str:
    """Convert common model labels to farmer-friendly names."""

    if language != "hi":
        return disease

    translations = {
        "wheat_stripe_rust": "गेहूं स्ट्राइप रस्ट",
        "wheat_septoria": "गेहूं सेप्टोरिया",
        "rice_bacterial_blight": "धान बैक्टीरियल ब्लाइट",
        "rice_brown_spot": "धान ब्राउन स्पॉट",
        "rice_tungro": "धान टुंग्रो",
        "sugarcane_mosaic": "गन्ना मोज़ेक रोग",
        "sugarcane_red_rot": "गन्ना लाल सड़न",
        "sugarcane_rust": "गन्ना रस्ट",
        "sugarcane_yellow": "गन्ना येलो रोग",
        "potato_early_blight": "आलू अर्ली ब्लाइट",
        "potato_late_blight": "आलू लेट ब्लाइट",
        "tomato_bacterial_spot": "टमाटर बैक्टीरियल स्पॉट",
        "tomato_early_blight": "टमाटर अर्ली ब्लाइट",
    }

    normalized = disease.lower().replace(" ", "_")

    return translations.get(normalized, disease)


def predict(image_bytes: bytes, language: str) -> dict:
    """Run Roboflow inference and return the KisanAI disease response."""

    if not image_bytes:
        raise ValueError("Image cannot be empty.")

    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise ValueError("Invalid image data.") from exc

    result = _client.infer(
        image,
        model_id=ROBOFLOW_MODEL_ID,
    )

    disease, confidence = _extract_prediction(result)

    confidence_percentage = round(confidence * 100, 2)

    if not disease:
        if language == "hi":
            disease_name = "रोग की पहचान नहीं हो सकी"
        else:
            disease_name = "Disease could not be identified"

        return {
            "disease": disease_name,
            "confidence": 0,
            "low_confidence": True,
            "actions": _get_actions("", language),
        }

    disease_name = _translate_disease(disease, language)

    low_confidence = confidence_percentage < CONFIDENCE_THRESHOLD

    if low_confidence:
        if language == "hi":
            actions = [
                "एक साफ और अच्छी रोशनी वाली पत्ती की तस्वीर दोबारा अपलोड करें",
                "प्रभावित हिस्से की नज़दीक से तस्वीर लें",
                "उपचार से पहले स्थानीय कृषि विशेषज्ञ से सलाह लें",
            ]
        else:
            actions = [
                "Upload a clearer image in good lighting",
                "Take a closer photo of the affected area",
                "Consult a local agricultural expert before treatment",
            ]
    else:
        actions = _get_actions(disease, language)

    return {
        "disease": disease_name,
        "confidence": confidence_percentage,
        "low_confidence": low_confidence,
        "actions": actions,
    }