import React from "react";
import { Badge } from "./Badge";

export function StatusBadge({ status = "Completed" }) {
  const normalized = status.toLowerCase();

  if (normalized === "completed") {
    return (
      <Badge variant="teal" dot>
        Completed
      </Badge>
    );
  }

  if (normalized === "in progress" || normalized === "analyzing") {
    return (
      <Badge variant="blue" dot>
        In Progress
      </Badge>
    );
  }

  if (normalized === "needs review" || normalized === "urgent") {
    return (
      <Badge variant="amber" dot>
        Follow-up Required
      </Badge>
    );
  }

  return <Badge variant="slate">{status}</Badge>;
}
