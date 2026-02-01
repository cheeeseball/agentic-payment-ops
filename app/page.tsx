import AreaChart from "@/components/AreaChart";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import BankCards from "@/components/BankTable";

export default function Home() {
  return (
    <main className="max-w-full">
      <Header />
      <Hero />
      <div className="min-h-20"></div>
      <section id="banks" className="px-10 py-16">
        <BankCards />
      </section>
      <div className="min-h-20"></div>
    </main>

  );
}