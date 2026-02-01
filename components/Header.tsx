"use client";

import Link from "next/link";
import { Search } from "lucide-react";
import { ChartBarIcon } from "@heroicons/react/24/solid";

export default function Header() {
  return (
    <header className="
      w-[95%] h-16 mx-auto mt-4 px-6
      flex items-center justify-between
      text-white
      bg-white/5 backdrop-blur-xl
      border border-white/10
      rounded-2xl shadow-lg
    ">
      
      {/* Left: Logo */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center">
          <ChartBarIcon className="w-5 h-5 text-black" />
        </div>
        <span className="font-league font-black tracking-wide">
          FirmPay
        </span>
      </div>

      {/* Center: Nav */}
      <nav className="flex items-center gap-6 text-sm text-gray-300">
        <a href="#banks" className="hover:text-white">
          Banks
        </a>

        <Link href="/transactions" className="hover:text-white">
          Transactions
        </Link>
      </nav>

      {/* Right: Search */}
      <div className="flex items-center gap-4">
        <div className="relative">
          <input
            type="text"
            placeholder="Search..."
            className="
              w-64 pl-4 pr-10 py-2 rounded-full
              bg-black/40
              border border-white/10
              focus:outline-none focus:border-white/30
              text-sm
            "
          />
          <Search className="w-4 h-4 absolute right-3 top-2.5 text-gray-400" />
        </div>
      </div>
    </header>
  );
}
