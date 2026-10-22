/**
 * Central API Client for Healix FastAPI Backend.
 * Correctly distinguishes network failures, 401 unauthorized, 422 validation,
 * and server errors without swallowing exceptions or logging sensitive patient text.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

export class ApiError extends Error {
  constructor(message, status = 500, data = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
    this.isUnauthorized = status === 401;
    this.isForbidden = status === 403;
    this.isNotFound = status === 404;
    this.isValidationError = status === 422;
    this.isNetworkError = status === 0;
  }
}

export async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = localStorage.getItem("healix_token");

  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  let response;
  try {
    response = await fetch(url, { ...options, headers });
  } catch (err) {
    // True network failure / offline
    throw new ApiError(
      "Unable to connect to Healix server. Please check your internet connection.",
      0,
      { originalError: err.message }
    );
  }

  // Handle unauthorized
  if (response.status === 401) {
    throw new ApiError("Session expired or authentication required.", 401);
  }

  // Parse JSON response body if possible
  let data = null;
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    try {
      data = await response.json();
    } catch {
      data = null;
    }
  } else {
    try {
      data = await response.text();
    } catch {
      data = null;
    }
  }

  if (!response.ok) {
    const errorMsg =
      (data && (data.message || data.detail)) ||
      `Request failed with status ${response.status}`;
    throw new ApiError(typeof errorMsg === "string" ? errorMsg : JSON.stringify(errorMsg), response.status, data);
  }

  return data;
}

export { API_BASE_URL };
