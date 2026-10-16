import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { assessmentService } from "../services/assessmentService";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { UrgencyIndicator } from "../components/common/UrgencyIndicator";
import {
  FileText,
  Printer,
  ChevronRight,
  Calendar,
  Download,
  Stethoscope,
  ShieldCheck,
  PlusCircle,
} from "lucide-react";

export function ReportsOverviewPage() {
  const [assessments, setAssessments] = useState([]);

  useEffect(() => {
    const list = assessmentService.getAllAssessments();
    setAssessments(list);
  }, []);

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
            <FileText className="w-7 h-7 text-teal-600" />
            Clinical Intake Reports
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Doctor-ready printable medical briefs consolidating symptoms, timeline, and intake answers.
          </p>
        </div>

        <Link to="/symptom-checker">
          <Button variant="teal" size="sm" icon={PlusCircle}>
            New Assessment
          </Button>
        </Link>
      </div>

      {/* Reports List */}
      <div className="space-y-4">
        {assessments.map((asm) => (
          <Card key={asm.id} padding="default" hover className="transition-all">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-slate-400">REF: {asm.id}</span>
                  <UrgencyIndicator
                    level={asm.urgencyLevel}
                    title={asm.urgencyLevel === "emergency" ? "Emergency" : asm.urgencyLevel === "urgent" ? "Urgent" : "Routine"}
                    compact
                  />
                </div>
                <h3 className="text-base font-bold text-slate-900">
                  {asm.primarySymptom || asm.symptoms?.join(", ")}
                </h3>
                <div className="flex items-center gap-2 text-xs text-slate-500">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3.5 h-3.5 text-slate-400" />
                    {asm.date}
                  </span>
                  <span>•</span>
                  <span>{asm.symptoms?.length || 0} Symptoms Analyzed</span>
                </div>
              </div>

              <div className="flex items-center gap-2.5 shrink-0 pt-2 sm:pt-0">
                <Link to={`/report/${asm.id}`}>
                  <Button variant="teal" size="sm" icon={Printer}>
                    Print Brief
                  </Button>
                </Link>
                <Link to={`/assessment/${asm.id}`}>
                  <Button variant="outline" size="sm" icon={ChevronRight} iconPosition="right">
                    View Summary
                  </Button>
                </Link>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
