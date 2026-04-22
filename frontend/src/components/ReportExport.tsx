"use client";

import { useState } from 'react';
import { generateReport } from '../lib/api';

export function ReportExport({ ideaId }: { ideaId: string }) {
  const [artifact, setArtifact] = useState<string | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<'pdf' | 'csv' | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onExport(format: 'pdf' | 'csv') {
    try {
      setLoading(format);
      setError(null);
      const result = await generateReport({ idea_id: ideaId, format });
      setArtifact(result.artifact_path);
      setDownloadUrl(result.download_url ?? null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate report');
    } finally {
      setLoading(null);
    }
  }

  return (
    <div className="card">
      <div className="card-body">
        <h3 className="font-semibold">Export Report</h3>
        <div className="mt-3 flex flex-wrap gap-3">
          <button className="rounded bg-slate-100 px-3 py-2 text-slate-950 disabled:opacity-60" disabled={loading !== null} onClick={() => onExport('pdf')}>
            {loading === 'pdf' ? 'Generating PDF...' : 'PDF'}
          </button>
          <button className="rounded bg-slate-100 px-3 py-2 text-slate-950 disabled:opacity-60" disabled={loading !== null} onClick={() => onExport('csv')}>
            {loading === 'csv' ? 'Generating CSV...' : 'CSV'}
          </button>
          {downloadUrl ? (
            <a className="rounded border border-emerald-500 px-3 py-2 text-emerald-300" href={downloadUrl} target="_blank" rel="noreferrer">
              Download file
            </a>
          ) : null}
        </div>
        {artifact ? <p className="mt-3 text-sm text-slate-300">Generated: {artifact}</p> : null}
        {error ? <p className="mt-3 text-sm text-rose-300">{error}</p> : null}
      </div>
    </div>
  );
}
