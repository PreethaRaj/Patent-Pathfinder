import { fetchProjects, type ProjectSummary } from '../../lib/api';

export default async function ProjectsPage() {
  let projects: ProjectSummary[] = [];
  let error: string | null = null;

  try {
    projects = await fetchProjects();
  } catch (err) {
    error = err instanceof Error ? err.message : 'Failed to load projects';
  }

  return (
    <main className="app-shell space-y-6">
      <section className="card">
        <div className="card-body">
          <h1 className="text-3xl font-bold">Projects</h1>
          <p className="mt-2 text-slate-300">Saved project summaries from the backend.</p>
        </div>
      </section>

      <section className="card">
        <div className="card-body">
          {error ? <p className="text-rose-300">{error}</p> : null}
          {!error && !projects.length ? <p className="text-slate-400">No projects available.</p> : null}
          <div className="space-y-3">
            {projects.map((project) => (
              <div key={project.project_id} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
                <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                  <div>
                    <div className="font-semibold">{project.title}</div>
                    <div className="text-sm text-slate-400">{project.domain}</div>
                  </div>
                  <div className="text-sm text-slate-300">{project.status}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
