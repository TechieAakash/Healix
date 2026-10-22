import { assessmentService } from "./assessmentService";

export const historyService = {
  async getHistory() {
    return await assessmentService.getAllAssessments();
  },

  async filterHistory({ filter = "all", searchQuery = "" }) {
    const list = await this.getHistory();
    const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);

    return list.filter((item) => {
      // Filter by urgency or timeframe
      if (filter === "recent") {
        const itemDate = new Date(item.date || item.createdAt);
        if (!isNaN(itemDate.getTime()) && itemDate < sevenDaysAgo) {
          return false;
        }
      } else if (filter === "urgent") {
        const level = (item.urgencyLevel || "").toLowerCase();
        if (level !== "urgent" && level !== "emergency") return false;
      } else if (filter === "routine") {
        const level = (item.urgencyLevel || "").toLowerCase();
        if (level !== "routine" && level !== "self-care" && level !== "low") return false;
      } else if (filter === "completed") {
        if (item.status !== "Completed" && item.status !== "COMPLETED") return false;
      }

      // Filter by search query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const symptomStr = Array.isArray(item.symptoms) ? item.symptoms.join(" ") : "";
        const text = `${item.primarySymptom || ""} ${symptomStr} ${item.urgencyTitle || ""}`.toLowerCase();
        if (!text.includes(q)) return false;
      }

      return true;
    });
  },
};
