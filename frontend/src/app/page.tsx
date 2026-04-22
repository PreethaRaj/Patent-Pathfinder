import Link from "next/link";

export default function HomePage() {
  return (
    <main className="mx-auto max-w-6xl space-y-8 p-8">
      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-8">
        <div className="max-w-4xl">
          <p className="text-sm uppercase tracking-[0.2em] text-emerald-400">MCP-first innovation analysis</p>
          <h1 className="mt-3 text-4xl font-bold">Intelligent Innovation Copilot</h1>
          <p className="mt-4 text-lg text-slate-300">
            Analyze invention ideas, retrieve prior art, highlight feature-level novelty, and export evidence-backed reports using local models and switchable patent data sources.
          </p>
          <div className="mt-6 flex flex-wrap gap-4">
            <Link className="rounded bg-emerald-500 px-4 py-2 font-medium text-slate-950" href="/idea-input">Start analysis</Link>
            <Link className="rounded border border-slate-700 px-4 py-2" href="/results">See latest results</Link>
            <Link className="rounded border border-slate-700 px-4 py-2" href="/projects">Browse projects</Link>
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {[
          {
            title: "Feature decomposition",
            body: "Break ideas into technical features and map each one to evidence passages and saturation levels.",
          },
          {
            title: "Patent-source switching",
            body: "Run in demo mode for seeded walkthroughs or switch to Lens-backed retrieval when the token is available.",
          },
          {
            title: "Report export",
            body: "Generate PDF or CSV artifacts for review, sharing, and project documentation.",
          },
        ].map((card) => (
          <div key={card.title} className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold">{card.title}</h2>
            <p className="mt-3 text-sm text-slate-300">{card.body}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
