"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';

import { analyzeIdea, type IdeaPayload } from '../lib/api';
import { saveIdeaResult } from '../lib/session';

const demoIdea: IdeaPayload = {
  title: 'Warehouse Stockout Prediction',
  problem_statement:
    'I want an AI system that predicts warehouse stockouts using camera feeds from shelves and ERP inventory signals. The model should alert managers when a shelf is empty before the ERP catches up.',
  domain: 'retail-operations',
  objectives: ['Real-time stockout prediction', 'Pre-ERP alerting'],
  constraints: ['Edge deployment', 'Low latency'],
  tags: ['AI', 'computer-vision', 'logistics'],
  source: 'demo',
};

export function IdeaEditor() {
  const router = useRouter();
  const [payload, setPayload] = useState<IdeaPayload>({
    title: '',
    problem_statement: '',
    domain: 'general',
    objectives: [],
    constraints: [],
    tags: [],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function onChange<K extends keyof IdeaPayload>(key: K, value: IdeaPayload[K]) {
    setPayload((current) => ({ ...current, [key]: value }));
  }

  async function onAnalyze() {
    try {
      setLoading(true);
      setError(null);
      const result = await analyzeIdea(payload);
      saveIdeaResult(result);
      router.push('/results');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze idea');
    } finally {
      setLoading(false);
    }
  }

  function loadDemo() {
    setPayload(demoIdea);
    setError(null);
  }

  return (
    <div className="card">
      <div className="card-body space-y-4">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="text-2xl font-semibold">Analyze innovation idea</h2>
            <p className="mt-1 text-sm text-slate-300">Submit an idea to retrieve prior art, novelty signals, CPC guidance, and redesign suggestions.</p>
          </div>
          <button type="button" onClick={loadDemo} className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-100 hover:bg-slate-800">
            Load seeded demo
          </button>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <label className="space-y-2">
            <span className="text-sm text-slate-300">Idea title</span>
            <input className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" value={payload.title} onChange={(e) => onChange('title', e.target.value)} />
          </label>
          <label className="space-y-2">
            <span className="text-sm text-slate-300">Domain</span>
            <input className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" value={payload.domain} onChange={(e) => onChange('domain', e.target.value)} />
          </label>
        </div>

        <label className="block space-y-2">
          <span className="text-sm text-slate-300">Problem statement</span>
          <textarea className="min-h-40 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" value={payload.problem_statement} onChange={(e) => onChange('problem_statement', e.target.value)} />
        </label>

        <div className="grid gap-4 md:grid-cols-3">
          <label className="space-y-2">
            <span className="text-sm text-slate-300">Objectives (comma separated)</span>
            <input className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" value={(payload.objectives ?? []).join(', ')} onChange={(e) => onChange('objectives', e.target.value.split(',').map((x) => x.trim()).filter(Boolean))} />
          </label>
          <label className="space-y-2">
            <span className="text-sm text-slate-300">Constraints (comma separated)</span>
            <input className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" value={(payload.constraints ?? []).join(', ')} onChange={(e) => onChange('constraints', e.target.value.split(',').map((x) => x.trim()).filter(Boolean))} />
          </label>
          <label className="space-y-2">
            <span className="text-sm text-slate-300">Tags (comma separated)</span>
            <input className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" value={(payload.tags ?? []).join(', ')} onChange={(e) => onChange('tags', e.target.value.split(',').map((x) => x.trim()).filter(Boolean))} />
          </label>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row">
          <button type="button" onClick={onAnalyze} disabled={loading || !payload.title || !payload.problem_statement} className="rounded-lg bg-emerald-500 px-4 py-2 font-medium text-slate-950 disabled:cursor-not-allowed disabled:opacity-60">
            {loading ? 'Analyzing...' : 'Run analysis'}
          </button>
        </div>

        {error ? <p className="text-sm text-rose-300">{error}</p> : null}
      </div>
    </div>
  );
}
