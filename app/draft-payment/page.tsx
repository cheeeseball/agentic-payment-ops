"use client";

import { useEffect, useState } from "react";

type Draft = {
    id: number;
    txn_id: string;
    bank_name: string;
    amount: number;
    method: string;
    status: string;
    error_code: string | null;
    latency_ms: number;
    created_at: string;
};

export default function DraftsPage() {
    const [drafts, setDrafts] = useState<Draft[]>([]);

    useEffect(() => {
        fetch("/api/drafts")
            .then((res) => res.json())
            .then(setDrafts);
    }, []);

    // const startProcessing = async () => {
    //     await fetch("/api/start-processing", {
    //         method: "POST",
    //     });
    // };

    const startProcessing = async () => {
        console.log("BUTTON CLICKED");
        const res = await fetch("/api/start-processing", { method: "POST" });
        const data = await res.text();
        console.log("API RESPONSE:", data);
    };

    return (
        <main className="min-h-screen bg-black p-10">
            <h1 className="text-3xl font-league text-white mb-6">
                Draft Payments
            </h1>

            <p className="text-gray-400 mb-4">
                These payments are generated but not yet processed by the FirmPay AI.
            </p>

            <div className="bg-neutral-900 rounded-2xl border border-neutral-800 overflow-hidden">
                <table className="w-full text-sm text-white">
                    <thead className="bg-neutral-950 text-gray-400">
                        <tr>
                            <th className="p-4 text-left">Txn ID</th>
                            <th className="p-4 text-left">Bank</th>
                            <th className="p-4 text-left">Amount</th>
                            <th className="p-4 text-left">Method</th>
                            <th className="p-4 text-left">Latency</th>
                            <th className="p-4 text-left">Status</th>
                        </tr>
                    </thead>

                    <tbody>
                        {drafts.map((txn) => (
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
                                    <span className="px-3 py-1 rounded-full text-xs bg-blue-500/20 text-blue-400">
                                        {txn.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Start Processing Button (next step) */}
            <div className="mt-6">
                <button
                    onClick={startProcessing} className="bg-white text-black px-6 py-2 rounded-lg font-semibold hover:bg-gray-200 transition"
                >
                    Start Processing Payments
                </button>
            </div>
        </main>
    );
}
