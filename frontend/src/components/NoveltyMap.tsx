type NoveltyMapProps = {
  highSaturation: string[];
  moderateSaturation: string[];
  hotspots: string[];
};

function Badge({ children, tone }: { children: React.ReactNode; tone: 'amber' | 'blue' | 'emerald' }) {
  const classes = {
    amber: 'border-amber-700 bg-amber-950 text-amber-200',
    blue: 'border-sky-700 bg-sky-950 text-sky-200',
    emerald: 'border-emerald-700 bg-emerald-950 text-emerald-200',
  }[tone];
  return <span className={`rounded-full border px-3 py-1 text-sm ${classes}`}>{children}</span>;
}

export function NoveltyMap({ highSaturation, moderateSaturation, hotspots }: NoveltyMapProps) {
  return (
    <div className="card">
      <div className="card-body space-y-4">
        <div>
          <h3 className="text-xl font-semibold">Novelty Map</h3>
          <p className="mt-2 text-sm text-slate-300">Mapped feature saturation based on retrieved prior art and feature overlap scoring.</p>
        </div>

        <div className="space-y-3">
          <div className="flex flex-wrap gap-2">
            {highSaturation.map((id) => (
              <Badge key={`high-${id}`} tone="amber">{id} · high saturation</Badge>
            ))}
            {moderateSaturation.map((id) => (
              <Badge key={`moderate-${id}`} tone="blue">{id} · moderate saturation</Badge>
            ))}
            {hotspots.map((id) => (
              <Badge key={`hotspot-${id}`} tone="emerald">{id} · potential novelty hotspot</Badge>
            ))}
          </div>
          {!highSaturation.length && !moderateSaturation.length && !hotspots.length ? (
            <p className="text-sm text-slate-400">No novelty-map data is available.</p>
          ) : null}
        </div>
      </div>
    </div>
  );
}
