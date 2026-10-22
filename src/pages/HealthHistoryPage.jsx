import React, { useState, useEffect } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { historyService } from "../services/historyService";
import { AssessmentCard } from "../components/dashboard/AssessmentCard";
import { SkeletonLoader } from "../components/common/SkeletonLoader";
import { EmptyState } from "../components/common/EmptyState";
import { Button } from "../components/common/Button";
import { Card } from "../components/common/Card";
import {
  History,
  Search,
  PlusCircle,
} from "lucide-react";

export function HealthHistoryPage() {
  const [searchParams] = useSearchParams();
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState("all"); // 'all' | 'recent' | 'urgent' | 'completed'
  const [searchQuery, setSearchQuery] = useState(searchParams.get("q") || "");

  useEffect(() => {
    let isCurrent = true;
    historyService
      .filterHistory({ filter: activeFilter, searchQuery })
      .then((data) => {
        if (isCurrent) setAssessments(data);
      })
      .catch((e) => {
        console.error("Failed to load history:", e);
      })
      .finally(() => {
        if (isCurrent) setLoading(false);
      });

    return () => {
      isCurrent = false;
    };
  }, [activeFilter, searchQuery]);

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Page Title & Top CTA */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
            <History className="w-7 h-7 text-emerald-700" />
            Health History Log
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Review previous triage assessments, reported symptoms, and printable summaries.
          </p>
        </div>

        <Link to="/symptom-checker">
          <Button variant="primary" size="sm" icon={PlusCircle}>
            New Assessment
          </Button>
        </Link>
      </div>

      {/* Filter and Search Bar */}
      <Card padding="sm" className="space-y-3">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          {/* Filter Pills */}
          <div className="flex items-center gap-1.5 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
            {[
              { id: "all", label: "All Records" },
              { id: "recent", label: "Recent" },
              { id: "urgent", label: "Urgent Attention" },
              { id: "completed", label: "Completed" },
            ].map((f) => (
              <button
                key={f.id}
                onClick={() => setActiveFilter(f.id)}
                className={`text-xs px-3 py-1.5 rounded-xl font-medium transition-all whitespace-nowrap cursor-pointer ${
                  activeFilter === f.id
                    ? "bg-slate-900 text-white shadow-xs font-semibold"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>

          {/* Search field */}
          <div className="relative w-full sm:w-64">
            <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              placeholder="Search symptoms..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl pl-8 pr-3 py-1.5 outline-none focus:border-emerald-600 focus:bg-white"
            />
          </div>
        </div>
      </Card>

      {/* Main Content Area */}
      {loading ? (
        <SkeletonLoader type="card" count={3} />
      ) : assessments.length === 0 ? (
        <EmptyState
          title="No health assessments yet"
          description={
            searchQuery
              ? `No assessments matched "${searchQuery}". Try a different keyword.`
              : "You haven't conducted any symptom checks yet. Describe your symptoms to get started."
          }
          actionLabel="Start your first assessment"
          onAction={() => window.location.assign("/symptom-checker")}
        />
      ) : (
        <div className="space-y-4">
          {assessments.map((item) => (
            <div key={item.id} className="relative group">
              <AssessmentCard assessment={item} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
