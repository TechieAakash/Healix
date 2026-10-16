import { assessmentService } from "./assessmentService";
import { apiRequest } from "./apiClient";

export const historyService = {
  async getHistory() {
    const res = await apiRequest("/history");
    if (res && Array.isArray(res)) return res;
    return assessmentService.getAllAssessments();
  },

  async filterHistory({ filter = "all", searchQuery = "" }) {
    const list = await this.getHistory();
    return list.filter((item) => {
      // Filter by urgency or status
      if (filter === "urgent" && item.urgencyLevel !== "urgent") return false;
      if (filter === "routine" && item.urgencyLevel !== "routine") return false;
      if (filter === "completed" && item.status !== "Completed") return false;

      // Filter by search query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const text = `${item.primarySymptom} ${item.symptoms.join(" ")} ${item.urgencyTitle}`.toLowerCase();
        if (!text.includes(q)) return false;
      }

      return true;
    });
  },

  async deleteRecord(id) {
    const list = assessmentService.getAllAssessments();
    const updated = list.filter((item) => item.id !== id);
    localStorage.setItem("healix_assessments", JSON.stringify(updated));
    return updated;
  },
};
