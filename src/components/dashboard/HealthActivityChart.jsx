import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";
import { mockHealthActivityData } from "../../data/mockData";

function CustomTooltip({ active, payload, label }) {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-900 text-white p-3 rounded-xl shadow-lg text-xs space-y-1 border border-slate-800">
        <p className="font-semibold text-slate-200">{label}</p>
        <p className="text-teal-400">
          Check-ins: <span className="font-medium text-white">{payload[0]?.value}</span>
        </p>
        <p className="text-blue-300">
          Fatigue Index (1-5): <span className="font-medium text-white">{payload[1]?.value}</span>
        </p>
        <p className="text-amber-300">
          Discomfort Level (1-5): <span className="font-medium text-white">{payload[2]?.value}</span>
        </p>
      </div>
    );
  }
  return null;
}

export function HealthActivityChart({ data = mockHealthActivityData }) {
  return (
    <div className="w-full h-64 sm:h-72">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
          <XAxis
            dataKey="week"
            tick={{ fontSize: 11, fill: "#64748b" }}
            axisLine={{ stroke: "#e5e5ea" }}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 11, fill: "#64748b" }}
            axisLine={false}
            tickLine={false}
            domain={[0, 6]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            verticalAlign="top"
            align="right"
            iconType="circle"
            wrapperStyle={{ paddingBottom: 16, fontSize: 12 }}
          />
          <Line
            type="monotone"
            name="Check-ins"
            dataKey="checkins"
            stroke="#0d9488"
            strokeWidth={2.5}
            dot={{ r: 3, fill: "#0d9488" }}
            activeDot={{ r: 5 }}
          />
          <Line
            type="monotone"
            name="Reported Fatigue"
            dataKey="fatigueLevel"
            stroke="#6366f1"
            strokeWidth={2}
            strokeDasharray="4 4"
            dot={{ r: 2.5, fill: "#6366f1" }}
          />
          <Line
            type="monotone"
            name="Discomfort Index"
            dataKey="painIntensity"
            stroke="#f59e0b"
            strokeWidth={2}
            dot={{ r: 2.5, fill: "#f59e0b" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
