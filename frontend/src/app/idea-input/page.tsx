"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { analyzeIdea } from "../../lib/api";
import { saveIdeaPayload, saveIdeaResult } from "../../lib/session";


const demoIdea = {
  title: "Warehouse Stockout Prediction",
  problem_statement:
    "I want an AI system that predicts warehouse stockouts using camera feeds from shelves and ERP inventory signals. The model should alert managers when a shelf is empty before the ERP catches up.",
  domain: "retail-operations",
  objectives: ["Real-time stockout prediction", "Pre-ERP alerting"],
  constraints: ["Edge deployment", "Low latency"],
  tags: ["AI", "computer-vision", "logistics"],
};

export default function IdeaInputPage() {
  const router = useRouter();

  const [title, setTitle] = useState("");
  const [domain, setDomain] = useState("");
  const [problemStatement, setProblemStatement] = useState("");
  const [objectives, setObjectives] = useState("");
  const [constraints, setConstraints] = useState("");
  const [tags, setTags] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const parsedPreview = useMemo(
    () => ({
      objectives: objectives.split(",").map((x) => x.trim()).filter(Boolean),
      constraints: constraints.split(",").map((x) => x.trim()).filter(Boolean),
      tags: tags.split(",").map((x) => x.trim()).filter(Boolean),
    }),
    [objectives, constraints, tags]
  );

  const loadDemo = () => {
    setTitle(demoIdea.title);
    setDomain(demoIdea.domain);
    setProblemStatement(demoIdea.problem_statement);
    setObjectives(demoIdea.objectives.join(", "));
    setConstraints(demoIdea.constraints.join(", "));
    setTags(demoIdea.tags.join(", "));
    setError(null);
  };

  const handleAnalyze = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      const payload = {
        title: title.trim(),
        problem_statement: problemStatement.trim(),
        domain: domain.trim() || "general",
        objectives: objectives.split(",").map((x) => x.trim()).filter(Boolean),
        constraints: constraints.split(",").map((x) => x.trim()).filter(Boolean),
        tags: tags.split(",").map((x) => x.trim()).filter(Boolean),
      };

      if (!payload.title || !payload.problem_statement) {
        throw new Error("Title and problem statement are required.");
      }

      saveIdeaPayload(payload);
      const result = await analyzeIdea(payload);
      saveIdeaResult(result);

      router.push("/results");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to analyze idea.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="app-shell">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-emerald-400">
            Innovation Copilot
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            Analyze innovation idea
          </h1>
          <p className="mt-2 max-w-3xl text-slate-400">
            Submit an idea to the MCP-backed pipeline and review novelty,
            evidence, CPC suggestions, and redesign opportunities.
          </p>
        </div>

        <button type="button" onClick={loadDemo} className="btn-secondary">
          Load demo idea
        </button>
      </div>

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_360px]">
        <section className="card">
          <div className="card-body space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <label className="label" htmlFor="title">Idea title</label>
                <input
                  id="title"
                  className="input"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Interoperable Embedded Hearing Compensation..."
                />
              </div>

              <div>
                <label className="label" htmlFor="domain">Domain</label>
                <input
                  id="domain"
                  className="input"
                  value={domain}
                  onChange={(e) => setDomain(e.target.value)}
                  placeholder="audio, logistics, medtech..."
                />
              </div>
            </div>

            <div>
              <label className="label" htmlFor="problemStatement">Problem statement</label>
              <textarea
                id="problemStatement"
                className="textarea"
                value={problemStatement}
                onChange={(e) => setProblemStatement(e.target.value)}
                placeholder="Describe the invention, system behavior, inputs, outputs, constraints, and why it matters."
              />
            </div>

            <div className="grid gap-6 md:grid-cols-3">
              <div>
                <label className="label" htmlFor="objectives">Objectives</label>
                <input
                  id="objectives"
                  className="input"
                  value={objectives}
                  onChange={(e) => setObjectives(e.target.value)}
                  placeholder="Real-time prediction, early alerting"
                />
                <p className="helper mt-2">Comma-separated.</p>
              </div>

              <div>
                <label className="label" htmlFor="constraints">Constraints</label>
                <input
                  id="constraints"
                  className="input"
                  value={constraints}
                  onChange={(e) => setConstraints(e.target.value)}
                  placeholder="Edge deployment, low latency"
                />
                <p className="helper mt-2">Comma-separated.</p>
              </div>

              <div>
                <label className="label" htmlFor="tags">Tags</label>
                <input
                  id="tags"
                  className="input"
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
                  placeholder="AI, computer-vision, logistics"
                />
                <p className="helper mt-2">Comma-separated.</p>
              </div>
            </div>

            {error && (
              <div className="rounded-xl border border-red-800 bg-red-950/40 px-4 py-3 text-sm text-red-200">
                {error}
              </div>
            )}

            <div className="flex flex-col gap-3 sm:flex-row">
              <button
                type="button"
                onClick={handleAnalyze}
                disabled={isSubmitting}
                className="btn-primary"
              >
                {isSubmitting ? "Running analysis..." : "Run analysis"}
              </button>
            </div>
          </div>
        </section>

        <aside className="card">
          <div className="card-body">
            <h2 className="text-lg font-semibold">Input preview</h2>
            <p className="mt-2 text-sm text-slate-400">
              Review the normalized metadata that will be sent to the backend.
            </p>

            <div className="mt-6 space-y-5">
              <div>
                <div className="text-sm font-medium text-slate-200">Objectives</div>
                <div className="mt-2 flex flex-wrap gap-2">
                  {parsedPreview.objectives.length > 0 ? (
                    parsedPreview.objectives.map((item) => (
                      <span key={item} className="chip">{item}</span>
                    ))
                  ) : (
                    <span className="helper">No objectives added yet.</span>
                  )}
                </div>
              </div>

              <div>
                <div className="text-sm font-medium text-slate-200">Constraints</div>
                <div className="mt-2 flex flex-wrap gap-2">
                  {parsedPreview.constraints.length > 0 ? (
                    parsedPreview.constraints.map((item) => (
                      <span key={item} className="chip">{item}</span>
                    ))
                  ) : (
                    <span className="helper">No constraints added yet.</span>
                  )}
                </div>
              </div>

              <div>
                <div className="text-sm font-medium text-slate-200">Tags</div>
                <div className="mt-2 flex flex-wrap gap-2">
                  {parsedPreview.tags.length > 0 ? (
                    parsedPreview.tags.map((item) => (
                      <span key={item} className="chip">{item}</span>
                    ))
                  ) : (
                    <span className="helper">No tags added yet.</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </main>
  );
}