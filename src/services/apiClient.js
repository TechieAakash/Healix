// Central API client configured for future FastAPI backend integration
// Seamlessly falls back to rich mock data when backend is not connected

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = localStorage.getItem("healix_token");

  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  try {
    const response = await fetch(url, { ...options, headers });
    if (!response.ok) {
      throw new Error(`API call failed: ${response.statusText}`);
    }
    return await response.json();
  } catch (err) {
    // If backend isn't reachable, log warning and let caller handle mock fallback
    console.info(`[Healix API] ${endpoint} not reached (${err.message}). Using mock provider.`);
    return null;
  }
}

export { API_BASE_URL };
