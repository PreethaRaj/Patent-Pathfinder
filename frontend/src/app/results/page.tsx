"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';

import { EvidenceViewer } from '../../components/EvidenceViewer';
import { NoveltyMap } from '../../components/NoveltyMap';
import { ReportExport } from '../../components/ReportExport';
import { loadIdeaResult } from '../../lib/session';
import type { IdeaAnalysisResponse } from '../../lib/api';

export default function ResultsPage() {
  const [data, setData] = useState<IdeaAnalysisResponse | null>(null);

  useEffect(() => {
    setData(loadIdeaResult());
  }, []);

  if (!data) {
    return (
      <main className="app-shell space-y-6">
        <section className="card">
          <div className="card-body">
            <h1 className="text-2xl font-bold">No analysis loaded</h1>
            <p className="mt-2 text-slate-300">Run an analysis from the home page first.</p>
            <Link href="/" className="mt-4 inline-block rounded-lg bg-emerald-500 px-4 py-2 font-medium text-slate-950">Go to home</Link>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="app-shell space-y-6">
      <section className="card">
        <div className="card-body">
          <p className="text-sm uppercase tracking-[0.2em] text-emerald-400">Live analysis</p>
          <h1 className="mt-2 text-3xl font-bold">{data.title}</h1>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <div className="text-xs uppercase text-slate-500">Status</div>
              <div className="mt-1 text-lg font-semibold">{data.status}</div>
            </div>
            <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <div className="text-xs uppercase text-slate-500">Analysis mode</div>
              <div className="mt-1 text-lg font-semibold">{data.analysis_mode ?? 'unknown'}</div>
            </div>
            <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <div className="text-xs uppercase text-slate-500">Retrieval source</div>
              <div className="mt-1 text-lg font-semibold">{data.retrieval_source ?? 'unknown'}</div>
            </div>
          </div>
        </div>
      </section>

      <section className="card">
        <div className="card-body">
          <h2 className="text-xl font-semibold">Decomposed Features</h2>
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            {data.decomposed_features.map((feature) => (
              <div key={feature.id} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
                <div className="text-xs uppercase text-slate-500">{feature.id}</div>
                <div className="mt-1 font-medium">{feature.name}</div>
                <div className="mt-2 text-sm text-emerald-300">Novelty: {feature.novelty_label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-2">
        <section className="card">
          <div className="card-body">
            <h2 className="text-xl font-semibold">Top Prior Art</h2>
            <div className="mt-4 space-y-3">
              {data.top_prior_art.length ? data.top_prior_art.map((item) => (
                <div key={item.publication_number} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
                  <div className="font-medium">{item.publication_number}</div>
                  <div className="mt-1 text-slate-200">{item.title}</div>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-400">
                    {item.evidence.map((entry, idx) => <li key={`${item.publication_number}-${idx}`}>{entry}</li>)}
                  </ul>
                </div>
              )) : <p className="text-sm text-slate-400">No prior-art items were returned.</p>}
            </div>
          </div>
        </section>

        <section className="card">
          <div className="card-body">
            <h2 className="text-xl font-semibold">Feature-to-Evidence Mapping</h2>
            <div className="mt-4 space-y-3">
              {data.feature_to_evidence_mapping.length ? data.feature_to_evidence_mapping.map((item) => (
                <div key={item.feature_id} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div className="font-medium">{item.feature_id} · {item.feature_name}</div>
                    <span className="text-xs text-emerald-300">{item.overlap_label}</span>
                  </div>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-400">
                    {item.evidence.map((entry, idx) => <li key={`${item.feature_id}-${idx}`}>{entry}</li>)}
                  </ul>
                </div>
              )) : <p className="text-sm text-slate-400">No feature evidence mappings were returned.</p>}
            </div>
          </div>
        </section>
      </section>

      <NoveltyMap
        highSaturation={data.novelty_map?.high_saturation ?? []}
        moderateSaturation={data.novelty_map?.moderate_saturation ?? []}
        hotspots={data.novelty_map?.potential_novelty_hotspots ?? []}
      />

      <EvidenceViewer items={data.evidence ?? []} />

      <section className="grid gap-6 xl:grid-cols-2">
        <section className="card">
          <div className="card-body">
            <h2 className="text-xl font-semibold">Suggested CPC Codes</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {data.suggested_cpc_codes.length ? data.suggested_cpc_codes.map((code) => (
                <span key={code} className="rounded-full border border-sky-700 bg-sky-950 px-3 py-1 text-sm text-sky-200">{code}</span>
              )) : <p className="text-sm text-slate-400">No CPC suggestions were returned.</p>}
            </div>
            <h3 className="mt-6 text-lg font-semibold">Search expansions</h3>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-400">
              {data.suggested_search_expansions.map((entry, idx) => <li key={`exp-${idx}`}>{entry}</li>)}
            </ul>
          </div>
        </section>

        <section className="card">
          <div className="card-body">
            <h2 className="text-xl font-semibold">Redesign Suggestions</h2>
            <ol className="mt-4 list-decimal space-y-2 pl-5 text-slate-300">
              {data.redesign_suggestions.map((entry, idx) => <li key={`suggestion-${idx}`}>{entry}</li>)}
            </ol>
          </div>
        </section>
      </section>

      <ReportExport ideaId={data.idea_id} />
    </main>
  );
}
