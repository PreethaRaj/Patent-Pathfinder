type EvidenceItem = {
  source_id?: string;
  title: string;
  passage: string;
  citation: string;
  score: number;
};

export function EvidenceViewer({ items }: { items: EvidenceItem[] }) {
  if (!items.length) {
    return (
      <div className="card">
        <div className="card-body">
          <h3 className="text-xl font-semibold">Evidence</h3>
          <p className="mt-2 text-sm text-slate-400">No evidence passages are available for this run.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-body space-y-3">
        <h3 className="text-xl font-semibold">Evidence</h3>
        {items.map((item, idx) => (
          <div key={`${item.source_id ?? item.citation}-${idx}`} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <div className="flex items-center justify-between gap-3">
              <h4 className="font-semibold">{item.title}</h4>
              <span className="text-xs text-slate-400">{item.score.toFixed(2)}</span>
            </div>
            <p className="mt-2 text-sm text-slate-300">{item.passage}</p>
            <p className="mt-2 text-xs text-slate-500">{item.citation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
