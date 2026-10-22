import { apiRequest } from "./apiClient";
import { mockUser } from "../data/mockData";

export const authService = {
  async login(email, password) {
    // This will throw ApiError for bad credentials (401) — callers should catch
    const apiResult = await apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (apiResult && apiResult.access_token) {
      // Store token immediately so /auth/me request is authenticated
      localStorage.setItem("healix_token", apiResult.access_token);

      // Fetch profile — wrap in try/catch so a profile failure doesn't block sign-in
      let mappedUser = { ...mockUser, email };
      try {
        const userProfile = await apiRequest("/auth/me");
        if (userProfile) {
          mappedUser = {
            ...mockUser,
            id: userProfile.id,
            name: userProfile.name?.split(" ")[0] || "User",
            fullName: userProfile.name || email,
            email: userProfile.email || email,
            gender: userProfile.gender || "Not specified",
            dateOfBirth: userProfile.date_of_birth || null,
          };
        }
      } catch {
        // Profile fetch failed but token is valid — proceed with minimal user
      }

      localStorage.setItem("healix_user", JSON.stringify(mappedUser));
      return mappedUser;
    }

    // Should not reach here — apiRequest throws on non-2xx
    throw new Error("Login failed: unexpected server response.");
  },

  async signup(userData) {
    // Throws ApiError (409 CONFLICT) if email already exists
    await apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        name: userData.fullName || userData.name,
        email: userData.email,
        password: userData.password,
      }),
    });

    // Auto-login after successful registration
    return this.login(userData.email, userData.password);
  },

  async resetPassword(email) {
    try {
      const apiResult = await apiRequest("/auth/forgot-password", {
        method: "POST",
        body: JSON.stringify({ email }),
      });
      if (apiResult) return apiResult;
    } catch {
      // Endpoint may not exist yet
    }
    await new Promise((resolve) => setTimeout(resolve, 700));
    return { success: true, message: `If that email is registered, password reset instructions have been sent.` };
  },

  getCurrentUser() {
    const saved = localStorage.getItem("healix_user");
    const token = localStorage.getItem("healix_token");

    if (!token) {
      // Not authenticated — return null so auth guards work correctly
      return null;
    }

    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        // Merge with mockUser to ensure all UI fields (metrics, etc.) exist
        return { ...mockUser, ...parsed };
      } catch {
        return { ...mockUser };
      }
    }

    // Token exists but no stored profile — return default
    return { ...mockUser };
  },

  logout() {
    localStorage.removeItem("healix_token");
    localStorage.removeItem("healix_user");
    return true;
  },

  async updateProfile(updates) {
    const current = this.getCurrentUser() || mockUser;
    const updated = { ...current, ...updates };
    localStorage.setItem("healix_user", JSON.stringify(updated));
    return updated;
  },

  isAuthenticated() {
    return !!localStorage.getItem("healix_token");
  },
};
