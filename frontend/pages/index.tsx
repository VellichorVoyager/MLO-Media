import type { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>MLO Intelligence — Know what to do before your competitors do</title>
        <meta
          name="description"
          content="Real-time deal signals for mortgage loan officers. We tell you who to call, what to say, and why — based on market shifts."
        />
      </Head>

      <main className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center px-6 py-24">
        <h1 className="text-5xl font-bold text-center leading-tight mb-6">
          Know what to do <span className="text-emerald-400">before</span> your
          competitors do.
        </h1>

        <p className="text-lg text-gray-400 text-center max-w-xl mb-10">
          MLO Intelligence turns mortgage market news into instant, actionable
          deal signals — so you always know who to call, what to pitch, and when
          to move.
        </p>

        <div className="flex gap-4 flex-wrap justify-center mb-20">
          <Link
            href="/dashboard"
            className="bg-emerald-500 hover:bg-emerald-400 text-black font-semibold px-8 py-3 rounded-xl transition"
          >
            View Dashboard
          </Link>
          <a
            href="#pricing"
            className="border border-gray-600 hover:border-gray-400 text-white px-8 py-3 rounded-xl transition"
          >
            See Pricing
          </a>
        </div>

        {/* Signal types */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl w-full mb-24">
          {[
            {
              emoji: "📉",
              title: "Refi Opportunity",
              desc: "Rates drop → call your past refi clients before anyone else does.",
            },
            {
              emoji: "🏠",
              title: "Purchase Surge",
              desc: "Inventory rises → target first-time buyers with the right message.",
            },
            {
              emoji: "⚖️",
              title: "Regulation Alert",
              desc: "CFPB activity → adjust your compliance messaging instantly.",
            },
            {
              emoji: "🏦",
              title: "Lender Shift",
              desc: "Competitor moves → reposition your offer and win the deal.",
            },
          ].map(({ emoji, title, desc }) => (
            <div
              key={title}
              className="bg-gray-900 border border-gray-800 rounded-2xl p-6"
            >
              <div className="text-3xl mb-3">{emoji}</div>
              <h3 className="font-semibold text-white mb-1">{title}</h3>
              <p className="text-gray-400 text-sm">{desc}</p>
            </div>
          ))}
        </section>

        {/* Pricing */}
        <section id="pricing" className="max-w-4xl w-full">
          <h2 className="text-3xl font-bold text-center mb-10">Pricing</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {[
              {
                name: "Free",
                price: "$0",
                features: ["Daily digest", "Top 5 signals"],
                cta: "Get started",
                highlight: false,
              },
              {
                name: "Pro",
                price: "$29/mo",
                features: [
                  "Everything in Free",
                  "Full signal feed",
                  "Insights dashboard",
                ],
                cta: "Start Pro",
                highlight: true,
              },
              {
                name: "Elite",
                price: "$99/mo",
                features: [
                  "Everything in Pro",
                  "Lead signals",
                  "Priority alerts",
                ],
                cta: "Go Elite",
                highlight: false,
              },
            ].map(({ name, price, features, cta, highlight }) => (
              <div
                key={name}
                className={`rounded-2xl p-6 border ${
                  highlight
                    ? "border-emerald-500 bg-emerald-950"
                    : "border-gray-800 bg-gray-900"
                }`}
              >
                <h3 className="text-xl font-bold mb-1">{name}</h3>
                <p className="text-3xl font-extrabold text-emerald-400 mb-4">
                  {price}
                </p>
                <ul className="text-gray-400 text-sm space-y-2 mb-6">
                  {features.map((f) => (
                    <li key={f}>✓ {f}</li>
                  ))}
                </ul>
                <button className="w-full bg-emerald-500 hover:bg-emerald-400 text-black font-semibold py-2 rounded-xl transition">
                  {cta}
                </button>
              </div>
            ))}
          </div>
        </section>
      </main>
    </>
  );
};

export default Home;
