// Mock data standing in for backend/AI/RAG responses (per PRD section 23 —
// "cache demo data and provide graceful fallback for the hackathon demo").
// Swap these for real API calls once the backend/AI/RAG endpoints are ready.

export const farmer = {
  name: "Ramesh",
  nameHi: "रमेश",
  location: "Barabanki, Uttar Pradesh",
  locationHi: "बाराबंकी, उत्तर प्रदेश",
  crops: ["Wheat", "Sugarcane"],
  cropsHi: ["गेहूं", "गन्ना"],
};

export const alerts = [
  {
    id: "a1",
    level: "warning",
    text_en: "Rain expected in 2 days — delay pesticide spraying on wheat.",
    text_hi: "2 दिनों में बारिश की संभावना — गेहूं पर कीटनाशक छिड़काव टालें।",
  },
  {
    id: "a2",
    level: "info",
    text_en: "PM-KISAN next installment window opens this month.",
    text_hi: "PM-KISAN की अगली किस्त इस महीने आने वाली है।",
  },
];

export const actionPlan = [
  { id: "p1", done: false, text_en: "Delay spraying — rain expected Thursday", text_hi: "छिड़काव टालें — गुरुवार को बारिश संभव" },
  { id: "p2", done: false, text_en: "Check wheat leaves for yellow rust spots", text_hi: "गेहूं के पत्तों पर पीले धब्बे जांचें" },
  { id: "p3", done: true, text_en: "Irrigate sugarcane field (completed)", text_hi: "गन्ने के खेत की सिंचाई (पूर्ण)" },
];

export const chatSuggestions = [
  { en: "Why are my wheat leaves turning yellow?", hi: "मेरे गेहूं के पत्ते पीले क्यों हो रहे हैं?" },
  { en: "Best time to sow sugarcane?", hi: "गन्ना बोने का सही समय क्या है?" },
  { en: "How much urea for 1 acre wheat?", hi: "1 एकड़ गेहूं के लिए कितना यूरिया चाहिए?" },
];

export const mockChatReply = {
  en: "For yellowing wheat leaves, it's often nitrogen deficiency or early rust. Check the undersides of leaves for orange-yellow powdery spots. If found, that's likely yellow rust — avoid excess irrigation and consider a fungicide spray after confirming with the Disease Detection tool.",
  hi: "गेहूं की पत्तियों के पीले होने का कारण अक्सर नाइट्रोजन की कमी या शुरुआती रस्ट रोग होता है। पत्तियों के नीचे नारंगी-पीले पाउडर जैसे धब्बे जांचें। यदि मिलें, तो यह पीला रस्ट हो सकता है — अधिक सिंचाई से बचें और 'रोग जांच' टूल से पुष्टि के बाद फफूंदनाशक का छिड़काव करें।",
  sources: ["ICAR Wheat Advisory 2025", "State Agriculture Dept. Bulletin"],
};

export const diseaseClasses = [
  {
    id: "yellow_rust",
    name_en: "Wheat Yellow Rust",
    name_hi: "गेहूं पीला रस्ट",
    confidence: 87,
    actions_en: [
      "Avoid excess nitrogen and irrigation for now",
      "Apply a recommended fungicide (e.g. Propiconazole) within 3 days",
      "Isolate and monitor nearby plants for spread",
    ],
    actions_hi: [
      "अभी अधिक नाइट्रोजन और सिंचाई से बचें",
      "3 दिनों के भीतर अनुशंसित फफूंदनाशक (जैसे प्रोपिकोनाज़ोल) डालें",
      "आसपास के पौधों पर फैलाव के लिए नज़र रखें",
    ],
  },
];

export const supportedCrops = ["Wheat", "Rice", "Sugarcane", "Cotton", "Tomato", "Potato"];

export const weatherData = {
  location: "Barabanki, Uttar Pradesh",
  locationHi: "बाराबंकी, उत्तर प्रदेश",
  today: {
    tempC: 31,
    condition_en: "Partly cloudy",
    condition_hi: "आंशिक रूप से बादल",
    humidity: 68,
    windKmh: 12,
    rainChance: 40,
  },
  forecast: [
    { day_en: "Thu", day_hi: "गुरु", tempC: 30, rain: 70, condition: "rain" },
    { day_en: "Fri", day_hi: "शुक्र", tempC: 29, rain: 80, condition: "rain" },
    { day_en: "Sat", day_hi: "शनि", tempC: 32, rain: 20, condition: "cloud" },
    { day_en: "Sun", day_hi: "रवि", tempC: 34, rain: 5, condition: "sun" },
    { day_en: "Mon", day_hi: "सोम", tempC: 33, rain: 10, condition: "sun" },
  ],
  recommendation_en: "Rain is likely Thursday and Friday. Delay any pesticide or urea application until Saturday, and make sure field drainage channels are clear to avoid waterlogging.",
  recommendation_hi: "गुरुवार और शुक्रवार को बारिश संभव है। शनिवार तक कीटनाशक या यूरिया डालने से बचें, और जलभराव रोकने के लिए खेत की नालियां साफ रखें।",
};

export const schemes = [
  {
    id: "pm_kisan",
    name_en: "PM-KISAN",
    name_hi: "पीएम-किसान",
    summary_en: "Direct income support of ₹6,000/year for eligible farmer families.",
    summary_hi: "पात्र किसान परिवारों को ₹6,000/वर्ष की सीधी आय सहायता।",
    eligibility_en: ["Small and marginal farmer family", "Own cultivable land", "Valid land records"],
    eligibility_hi: ["छोटे और सीमांत किसान परिवार", "स्वयं की कृषि योग्य भूमि", "मान्य भूमि दस्तावेज़"],
    documents_en: ["Aadhaar card", "Land ownership papers", "Bank account details"],
    documents_hi: ["आधार कार्ड", "भूमि स्वामित्व कागजात", "बैंक खाता विवरण"],
    steps_en: ["Visit pmkisan.gov.in or nearest CSC", "Fill the registration form", "Submit documents for verification"],
    steps_hi: ["pmkisan.gov.in या नज़दीकी CSC पर जाएं", "पंजीकरण फॉर्म भरें", "सत्यापन के लिए दस्तावेज़ जमा करें"],
    source: "pmkisan.gov.in",
  },
  {
    id: "pmfby",
    name_en: "Pradhan Mantri Fasal Bima Yojana",
    name_hi: "प्रधानमंत्री फसल बीमा योजना",
    summary_en: "Crop insurance covering losses from natural calamities, pests and disease.",
    summary_hi: "प्राकृतिक आपदा, कीट और रोग से होने वाले नुकसान को कवर करने वाला फसल बीमा।",
    eligibility_en: ["All farmers growing notified crops", "Loanee and non-loanee farmers"],
    eligibility_hi: ["अधिसूचित फसल उगाने वाले सभी किसान", "ऋणी और गैर-ऋणी किसान"],
    documents_en: ["Aadhaar card", "Land records", "Bank passbook", "Sowing declaration"],
    documents_hi: ["आधार कार्ड", "भूमि रिकॉर्ड", "बैंक पासबुक", "बुवाई घोषणा पत्र"],
    steps_en: ["Apply via bank, CSC or pmfby.gov.in", "Pay the nominal premium share", "Report crop loss within 72 hours if it occurs"],
    steps_hi: ["बैंक, CSC या pmfby.gov.in के माध्यम से आवेदन करें", "मामूली प्रीमियम राशि जमा करें", "नुकसान होने पर 72 घंटे के भीतर सूचित करें"],
    source: "pmfby.gov.in",
  },
  {
    id: "kcc",
    name_en: "Kisan Credit Card",
    name_hi: "किसान क्रेडिट कार्ड",
    summary_en: "Low-interest credit for seeds, fertilizer and farm needs.",
    summary_hi: "बीज, उर्वरक और खेती की जरूरतों के लिए कम ब्याज़ पर ऋण।",
    eligibility_en: ["Farmers, tenant farmers and sharecroppers", "Self-Help Group members engaged in farming"],
    eligibility_hi: ["किसान, बटाईदार और काश्तकार", "खेती से जुड़े स्वयं सहायता समूह सदस्य"],
    documents_en: ["Aadhaar and ID proof", "Land documents", "Passport-size photo"],
    documents_hi: ["आधार और पहचान प्रमाण", "भूमि दस्तावेज़", "पासपोर्ट साइज़ फोटो"],
    steps_en: ["Visit nearest bank branch", "Fill KCC application form", "Bank verifies and issues card"],
    steps_hi: ["नज़दीकी बैंक शाखा में जाएं", "KCC आवेदन फॉर्म भरें", "बैंक सत्यापन के बाद कार्ड जारी करता है"],
    source: "Dept. of Agriculture & Farmers Welfare",
  },
];
