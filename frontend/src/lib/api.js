// Thin fetch wrapper around the KisanAI FastAPI backend.
// Base URL can be overridden with VITE_API_BASE_URL (see .env.example).

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request(path, { method = "GET", body, isFormData = false } = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: isFormData ? undefined : { "Content-Type": "application/json" },
    body: isFormData ? body : body ? JSON.stringify(body) : undefined,
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    // Non-JSON response body (e.g. empty) — leave data as null.
  }

  if (!response.ok) {
    const detail = data?.detail || `Request to ${path} failed (${response.status})`;
    throw new ApiError(detail, response.status);
  }

  return data;
}

export function getDashboard(language) {
  return request(`/api/v1/dashboard?language=${encodeURIComponent(language)}`);
}

export function getWeather(location, crop, language) {
  const params = new URLSearchParams({ location, language });
  if (crop) params.set("crop", crop);
  return request(`/api/v1/weather?${params.toString()}`);
}

export function sendChatMessage(message, language) {
  return request("/api/v1/chat", {
    method: "POST",
    body: { message, language },
  });
}

export function queryScheme(question, language) {
  return request("/api/v1/schemes/query", {
    method: "POST",
    body: { question, language },
  });
}

export function predictDisease(imageFile, language) {
  const formData = new FormData();
  formData.append("image", imageFile);
  formData.append("language", language);
  return request("/api/v1/disease/predict", {
    method: "POST",
    body: formData,
    isFormData: true,
  });
}

export { ApiError };
