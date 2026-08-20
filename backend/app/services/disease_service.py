"""Crop disease detection service.

MOCK IMPLEMENTATION. Replace `predict()` internals with a real inference
call to the trained CV model once it's ready. Keep the function signature
the same so routes/disease.py doesn't need to change.
"""

CONFIDENCE_THRESHOLD = 70

_MOCK_RESULT = {
    "en": {
        "disease": "Wheat Yellow Rust",
        "actions": [
            "Avoid excess nitrogen and irrigation for now",
            "Apply a recommended fungicide (e.g. Propiconazole) within 3 days",
            "Isolate and monitor nearby plants for spread",
        ],
    },
    "hi": {
        "disease": "गेहूं पीला रस्ट",
        "actions": [
            "अभी अधिक नाइट्रोजन और सिंचाई से बचें",
            "3 दिनों के भीतर अनुशंसित फफूंदनाशक (जैसे प्रोपिकोनाज़ोल) डालें",
            "आसपास के पौधों पर फैलाव के लिए नज़र रखें",
        ],
    },
}


def predict(image_bytes: bytes, language: str) -> dict:
    """Return {disease, confidence, low_confidence, actions} for a leaf image.

    TODO(AI/ML team): call the real model here, e.g.
        result = disease_model.predict(image_bytes)
        return {
            "disease": result.label,
            "confidence": result.confidence,
            "low_confidence": result.confidence < CONFIDENCE_THRESHOLD,
            "actions": get_actions_for(result.label, language),
        }
    """
    mock = _MOCK_RESULT.get(language, _MOCK_RESULT["en"])
    confidence = 87
    return {
        "disease": mock["disease"],
        "confidence": confidence,
        "low_confidence": confidence < CONFIDENCE_THRESHOLD,
        "actions": mock["actions"],
    }
