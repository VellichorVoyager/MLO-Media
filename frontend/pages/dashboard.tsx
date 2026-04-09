import type { NextPage, GetServerSideProps } from "next";
import Head from "next/head";

interface Signal {
  type: string;
  action: string;
}

interface Article {
  id: string;
  title: string;
  url: string;
  source: string;
  published_at: string;
  signals: Signal[];
}

interface Props {
  articles: Article[];
  error?: string;
}

const SIGNAL_EMOJI: Record<string, string> = {
  "Refi Opportunity": "📉",
  "Purchase Opportunity": "🏠",
  "Regulation Alert": "⚖️",
  "Lender Shift": "🏦",
};

function SignalCard({ signal }: { signal: Signal }) {
  return (
    <span className="inline-flex items-center gap-1 bg-emerald-900 border border-emerald-700 text-emerald-300 text-xs font-medium px-2.5 py-1 rounded-full">
      {SIGNAL_EMOJI[signal.type] ?? "🔔"} {signal.type}
    </span>
  );
}

function OpportunityPanel({ articles }: { articles: Article[] }) {
  const topSignals: Signal[] = articles
    .flatMap((a) => a.signals ?? [])
    .reduce<Signal[]>((acc, s) => {
      if (!acc.find((x) => x.type === s.type)) acc.push(s);
      return acc;
    }, []);

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-8">
      <h2 className="text-lg font-semibold text-white mb-4">
        🎯 Top Opportunities Today
      </h2>
      {topSignals.length === 0 ? (
        <p className="text-gray-500 text-sm">No signals detected yet.</p>
      ) : (
        <ul className="space-y-3">
          {topSignals.map((s) => (
            <li key={s.type} className="flex items-start gap-3">
              <span className="text-xl">{SIGNAL_EMOJI[s.type] ?? "🔔"}</span>
              <div>
                <p className="text-white font-medium text-sm">{s.type}</p>
                <p className="text-gray-400 text-sm">{s.action}</p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

const Dashboard: NextPage<Props> = ({ articles, error }) => {
  return (
    <>
      <Head>
        <title>Dashboard — MLO Intelligence</title>
      </Head>

      <div className="min-h-screen bg-gray-950 text-white px-6 py-12 max-w-5xl mx-auto">
        <header className="mb-10">
          <h1 className="text-3xl font-bold">MLO Intelligence Dashboard</h1>
          <p className="text-gray-400 mt-1">
            Real-time deal signals from across the mortgage market.
          </p>
        </header>

        {error && (
          <div className="bg-red-900 border border-red-700 text-red-300 rounded-xl p-4 mb-8 text-sm">
            {error}
          </div>
        )}

        <OpportunityPanel articles={articles} />

        <section>
          <h2 className="text-lg font-semibold text-white mb-4">📰 Signal Feed</h2>
          {articles.length === 0 ? (
            <p className="text-gray-500 text-sm">No articles with signals yet.</p>
          ) : (
            <ul className="space-y-4">
              {articles.map((article) => (
                <li
                  key={article.id}
                  className="bg-gray-900 border border-gray-800 rounded-2xl p-5"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <a
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-white font-semibold hover:text-emerald-400 transition line-clamp-2"
                      >
                        {article.title}
                      </a>
                      <p className="text-gray-500 text-xs mt-1">
                        {article.source} ·{" "}
                        {new Date(article.published_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  {article.signals && article.signals.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-3">
                      {article.signals.map((s) => (
                        <SignalCard key={s.type} signal={s} />
                      ))}
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </>
  );
};

export const getServerSideProps: GetServerSideProps<Props> = async () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

  try {
    const res = await fetch(`${apiUrl}/signals`);
    if (!res.ok) throw new Error(`API responded with ${res.status}`);
    const articles: Article[] = await res.json();
    return { props: { articles } };
  } catch (err) {
    return {
      props: {
        articles: [],
        error: `Could not load signals: ${(err as Error).message}`,
      },
    };
  }
};

export default Dashboard;
