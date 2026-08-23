# 🌾 KisanAI

> AI-powered agricultural assistance for Indian farmers.

KisanAI is an AI-powered agricultural assistant designed to help farmers make better decisions by bringing **agricultural guidance, government scheme information, real-time weather insights, and crop disease detection** into a single platform.

The application combines a modern React frontend with a FastAPI backend, Gemini-powered AI, RAG-based agricultural knowledge retrieval, Supabase PostgreSQL, OpenWeather data, and AI-based crop disease detection.

---

## 🚀 Features

### 🤖 AI Agricultural Assistant

Ask questions about farming and receive practical, easy-to-understand answers.

Examples:

- "My wheat crop is turning yellow. What should I do?"
- "How often should I irrigate my wheat crop?"
- "What are the best practices for growing wheat?"
- "My tomato plants have yellow spots on their leaves."

The assistant supports:

- Agricultural guidance
- Crop-specific questions
- Practical recommendations
- English and Hindi responses
- Knowledge-grounded responses using RAG

---

### 📚 RAG-Powered Knowledge Base

KisanAI uses **Retrieval-Augmented Generation (RAG)** to provide answers grounded in an agricultural knowledge base.

Instead of relying entirely on the LLM's general knowledge, relevant documents are retrieved before generating an answer.

Current knowledge includes:

- Crop information
- Disease information
- Government schemes

Example documents include:

- Wheat cultivation
- Wheat stripe rust
- PM-KISAN
- Pradhan Mantri Fasal Bima Yojana
- Kisan Credit Card

### RAG Pipeline

```text
User Question
      ↓
Embedding Generation
      ↓
Vector Similarity Search
      ↓
Relevant Knowledge Chunks
      ↓
Gemini
      ↓
Grounded Agricultural Response
