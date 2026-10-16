import { apiRequest } from "./apiClient";
import { mockUser } from "../data/mockData";

export const authService = {
  async login(email, password) {
    const apiResult = await apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (apiResult) {
      localStorage.setItem("healix_token", apiResult.token || "mock_jwt_token");
      localStorage.setItem("healix_user", JSON.stringify(apiResult.user));
      return apiResult.user;
    }

    // Mock response simulation
    await new Promise((resolve) => setTimeout(resolve, 600));
    const user = { ...mockUser, email: email || mockUser.email };
    localStorage.setItem("healix_token", "mock_jwt_aakash_2026");
    localStorage.setItem("healix_user", JSON.stringify(user));
    return user;
  },

  async signup(userData) {
    const apiResult = await apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify(userData),
    });

    if (apiResult) {
      localStorage.setItem("healix_token", apiResult.token || "mock_jwt_token");
      localStorage.setItem("healix_user", JSON.stringify(apiResult.user));
      return apiResult.user;
    }

    await new Promise((resolve) => setTimeout(resolve, 800));
    const user = {
      ...mockUser,
      name: userData.name || "Aakash",
      fullName: userData.name || "Aakash Sharma",
      email: userData.email,
    };
    localStorage.setItem("healix_token", "mock_jwt_aakash_2026");
    localStorage.setItem("healix_user", JSON.stringify(user));
    return user;
  },

  async resetPassword(email) {
    const apiResult = await apiRequest("/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    });

    if (apiResult) return apiResult;
    await new Promise((resolve) => setTimeout(resolve, 700));
    return { success: true, message: `Password reset instructions sent to ${email}` };
  },

  getCurrentUser() {
    const saved = localStorage.getItem("healix_user");
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        return mockUser;
      }
    }
    return mockUser;
  },

  logout() {
    localStorage.removeItem("healix_token");
    localStorage.removeItem("healix_user");
    return true;
  },

  async updateProfile(updates) {
    const current = this.getCurrentUser();
    const updated = { ...current, ...updates };
    localStorage.setItem("healix_user", JSON.stringify(updated));
    return updated;
  }
};
