"use client";

import AreaChart from "@/components/AreaChart";

export default function Hero() {
  return (
    <section className="relative w-screen min-h-[80vh] flex items-center justify-center bg-black text-white overflow-hidden">

      {/* Graph background */}
      <div className="absolute inset-0 opacity-70">
        <AreaChart />
      </div>

      {/* Subtle grid background */}
      <div className="absolute inset-0 bg-[radial-gradient(#ffffff15_1px,transparent_1px)] bg-[size:40px_40px] opacity-30" />

      {/* Content */}
      <div className="relative z-10 text-center max-w-4xl px-6">
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight bg-gradient-to-b from-white to-gray-400 bg-clip-text text-transparent">
          AI for Reliable Payment Operations
        </h1>

        <p className="mt-6 text-lg md:text-xl text-gray-400">
          Manage Transactions through Reliable and Quick Banking Systems
        </p>

        <div className="mt-10">
          <button className="px-8 py-3 rounded-lg bg-neutral-400 text-black font-medium hover:bg-gray-200 transition">
            Start Paying Safe
          </button>
        </div>
      </div>
    </section>
  );
}
