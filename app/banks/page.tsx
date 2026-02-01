"use client";

import { useEffect, useState } from "react";
import { CheckCircle, XCircle, Clock, Shield } from "lucide-react";

type Bank = {
  id: number;
  display_name: string;
  is_active: boolean;
  requires_human_approval: boolean;
  success_rate: number;
  avg_latency: number;
};

export default function BanksPage() {
  const [banks, setBanks] = useState<Bank[]>([]);

  useEffect(() => {
    fetch("/api/banks")
      .then((res) => res.json())
      .then(setBanks);
  }, []);

  return (
    <main className="min-h-screen bg-black p-10">
      <h1 className="text-3xl font-league text-white mb-8">
        Bank Operations Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {banks.map((bank) => (
          <div
            key={bank.id}
            className="bg-neutral-900 rounded-2xl p-6 border border-neutral-800 hover:border-neutral-600 transition"
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">
                {bank.display_name}
              </h2>

              {bank.is_active ? (
                <CheckCircle className="text-green-400 w-5 h-5" />
              ) : (
                <XCircle className="text-red-400 w-5 h-5" />
              )}
            </div>

            {/* Metrics */}
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Success Rate</span>
                <span
                  className={`font-medium ${
                    bank.success_rate > 0.95
                      ? "text-green-400"
                      : bank.success_rate > 0.9
                      ? "text-yellow-400"
                      : "text-red-400"
                  }`}
                >
                  {(bank.success_rate * 100).toFixed(2)}%
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-400">Latency</span>
                <span
                  className={`${
                    bank.avg_latency < 200
                      ? "text-green-400"
                      : bank.avg_latency < 400
                      ? "text-yellow-400"
                      : "text-red-400"
                  }`}
                >
                  {bank.avg_latency} ms
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-gray-400 flex items-center gap-1">
                  <Shield className="w-4 h-4" />
                  Human Approval
                </span>
                <input
                  type="checkbox"
                  checked={bank.requires_human_approval}
                  readOnly
                  className="w-4 h-4 accent-white"
                />
              </div>
            </div>

            {/* Footer badge */}
            <div className="mt-5">
              <span
                className={`inline-block px-3 py-1 text-xs rounded-full ${
                  bank.is_active
                    ? "bg-green-500/20 text-green-400"
                    : "bg-red-500/20 text-red-400"
                }`}
              >
                {bank.is_active ? "Active Route" : "Disabled Route"}
              </span>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
