"""Government scheme assistant service.

MOCK IMPLEMENTATION. `_SCHEMES` below is a small curated list standing in
for the real RAG pipeline (embeddings + vector search over scheme docs).
Replace `query()` internals once that's ready — keep the return shape the
same so routes/schemes.py doesn't need to change.
"""

_SCHEMES = [
    {
        "id": "pm_kisan",
        "name": {"en": "PM-KISAN", "hi": "पीएम-किसान"},
        "summary": {
            "en": "Direct income support of Rs 6,000/year for eligible farmer families.",
            "hi": "पात्र किसान परिवारों को Rs 6,000/वर्ष की सीधी आय सहायता।",
        },
        "eligibility": {
            "en": ["Small and marginal farmer family", "Own cultivable land", "Valid land records"],
            "hi": ["छोटे और सीमांत किसान परिवार", "स्वयं की कृषि योग्य भूमि", "मान्य भूमि दस्तावेज़"],
        },
        "documents": {
            "en": ["Aadhaar card", "Land ownership papers", "Bank account details"],
            "hi": ["आधार कार्ड", "भूमि स्वामित्व कागजात", "बैंक खाता विवरण"],
        },
        "steps": {
            "en": ["Visit pmkisan.gov.in or nearest CSC", "Fill the registration form", "Submit documents for verification"],
            "hi": ["pmkisan.gov.in या नज़दीकी CSC पर जाएं", "पंजीकरण फॉर्म भरें", "सत्यापन के लिए दस्तावेज़ जमा करें"],
        },
        "source": "pmkisan.gov.in",
        "keywords": ["income", "support", "kisan", "money", "cash"],
    },
    {
        "id": "pmfby",
        "name": {"en": "Pradhan Mantri Fasal Bima Yojana", "hi": "प्रधानमंत्री फसल बीमा योजना"},
        "summary": {
            "en": "Crop insurance covering losses from natural calamities, pests and disease.",
            "hi": "प्राकृतिक आपदा, कीट और रोग से होने वाले नुकसान को कवर करने वाला फसल बीमा।",
        },
        "eligibility": {
            "en": ["All farmers growing notified crops", "Loanee and non-loanee farmers"],
            "hi": ["अधिसूचित फसल उगाने वाले सभी किसान", "ऋणी और गैर-ऋणी किसान"],
        },
        "documents": {
            "en": ["Aadhaar card", "Land records", "Bank passbook", "Sowing declaration"],
            "hi": ["आधार कार्ड", "भूमि रिकॉर्ड", "बैंक पासबुक", "बुवाई घोषणा पत्र"],
        },
        "steps": {
            "en": ["Apply via bank, CSC or pmfby.gov.in", "Pay the nominal premium share", "Report crop loss within 72 hours if it occurs"],
            "hi": ["बैंक, CSC या pmfby.gov.in के माध्यम से आवेदन करें", "मामूली प्रीमियम राशि जमा करें", "नुकसान होने पर 72 घंटे के भीतर सूचित करें"],
        },
        "source": "pmfby.gov.in",
        "keywords": ["insurance", "crop loss", "damage", "flood", "drought"],
    },
    {
        "id": "kcc",
        "name": {"en": "Kisan Credit Card", "hi": "किसान क्रेडिट कार्ड"},
        "summary": {
            "en": "Low-interest credit for seeds, fertilizer and farm needs.",
            "hi": "बीज, उर्वरक और खेती की जरूरतों के लिए कम ब्याज़ पर ऋण।",
        },
        "eligibility": {
            "en": ["Farmers, tenant farmers and sharecroppers", "Self-Help Group members engaged in farming"],
            "hi": ["किसान, बटाईदार और काश्तकार", "खेती से जुड़े स्वयं सहायता समूह सदस्य"],
        },
        "documents": {
            "en": ["Aadhaar and ID proof", "Land documents", "Passport-size photo"],
            "hi": ["आधार और पहचान प्रमाण", "भूमि दस्तावेज़", "पासपोर्ट साइज़ फोटो"],
        },
        "steps": {
            "en": ["Visit nearest bank branch", "Fill KCC application form", "Bank verifies and issues card"],
            "hi": ["नज़दीकी बैंक शाखा में जाएं", "KCC आवेदन फॉर्म भरें", "बैंक सत्यापन के बाद कार्ड जारी करता है"],
        },
        "source": "Dept. of Agriculture & Farmers Welfare",
        "keywords": ["loan", "credit", "bank", "fertilizer", "seeds"],
    },
]

_FALLBACK_ANSWER = {
    "en": "Here are the government schemes that may be relevant to your question.",
    "hi": "आपके प्रश्न से संबंधित सरकारी योजनाएं यहां दी गई हैं।",
}


def query(question: str, language: str) -> dict:
    """Return {answer, schemes} for a farmer's scheme question.

    TODO(LLM/RAG team): replace this keyword match with real retrieval, e.g.
        chunks = vector_store.search(question, top_k=3)
        answer = llm_client.complete(build_grounded_prompt(question, chunks))
        return {"answer": answer.text, "schemes": chunks_to_schemes(chunks)}
    """
    q = question.lower()
    matched = [s for s in _SCHEMES if any(k in q for k in s["keywords"])]
    if not matched:
        matched = _SCHEMES  # fall back to showing everything curated

    schemes = [
        {
            "name": s["name"].get(language, s["name"]["en"]),
            "summary": s["summary"].get(language, s["summary"]["en"]),
            "eligibility": s["eligibility"].get(language, s["eligibility"]["en"]),
            "documents": s["documents"].get(language, s["documents"]["en"]),
            "steps": s["steps"].get(language, s["steps"]["en"]),
            "source": s["source"],
        }
        for s in matched
    ]
    return {
        "answer": _FALLBACK_ANSWER.get(language, _FALLBACK_ANSWER["en"]),
        "schemes": schemes,
    }
