"use client";

import { useEffect, useState } from "react";

type Transaction = {
  id: number;
  txn_id: string;
  bank_name: string;
  amount: number;
  method: string;
  status: string;
  latency_ms: number;
  created_at: string;
};

export default function TransactionsPage() {
  const [txns, setTxns] = useState<Transaction[]>([]);

  useEffect(() => {
    fetch("/api/transactions")
      .then((res) => res.json())
      .then(setTxns);
  }, []);

  return (
    <main className="min-h-screen bg-black p-10">
      <h1 className="text-3xl font-league text-white mb-6">
        Transactions
      </h1>

      <div className="bg-neutral-900 rounded-2xl border border-neutral-800 overflow-hidden">
        <table className="w-full text-sm text-white">
          <thead className="bg-neutral-950 text-gray-400">
            <tr>
              <th className="p-4 text-left">Txn ID</th>
              <th className="p-4 text-left">Bank</th>
              <th className="p-4 text-left">Amount</th>
              <th className="p-4 text-left">Method</th>
              <th className="p-4 text-left">Vendor</th>
              <th className="p-4 text-left">Phone</th>
              <th className="p-4 text-left">Latency</th>
              <th className="p-4 text-left">Status</th>
            </tr>
          </thead>

          <tbody>
            {txns.map((txn) => (
              <tr
                key={txn.id}
                className="border-t border-neutral-800 hover:bg-neutral-800/40"
              >
                <td className="p-4 font-mono text-xs">{txn.txn_id}</td>
                <td className="p-4">{txn.bank_name}</td>
                <td className="p-4 font-semibold">₹{txn.amount}</td>
                <td className="p-4">{txn.method}</td>
                <td className="p-4">{txn.latency_ms} ms</td>
                <td className="p-4">
                  <span className={`px-3 py-1 rounded-full text-xs ${
                    txn.status === "SUCCESS"
                      ? "bg-green-500/20 text-green-400"
                      : txn.status === "PENDING"
                      ? "bg-yellow-500/20 text-yellow-400"
                      : "bg-red-500/20 text-red-400"
                  }`}>
                    {txn.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
