export type IdeaPayload = {
  title: string;
  problem_statement: string;
  domain: string;
  objectives?: string[];
  constraints?: string[];
  tags?: string[];
  source?: string;
};

export type IdeaAnalysisResponse = {
  idea_id: string;
  title: string;
  status: string;
  created_at: string;
  analysis_mode?: string | null;
  retrieval_source?: string | null;
  evidence: Array<{
    source_id: string;
    source_type: string;
    title: string;
    passage: string;
    score: number;
    citation: string;
  }>;
  novelty?: {
    overlap_score: number;
    saturation_level: string;
    recommendations: string[];
    clusters: Array<Record<string, unknown>>;
  } | null;
  decomposed_features: Array<{ id: string; name: string; novelty_label: string }>;
  top_prior_art: Array<{ publication_number: string; title: string; evidence: string[] }>;
  feature_to_evidence_mapping: Array<{
    feature_id: string;
    feature_name: string;
    overlap_label: string;
    evidence: string[];
  }>;
  novelty_map: {
    high_saturation: string[];
    moderate_saturation: string[];
    potential_novelty_hotspots: string[];
  };
  redesign_suggestions: string[];
  suggested_cpc_codes: string[];
  suggested_search_expansions: string[];
};

export type ProjectSummary = {
  project_id: string;
  title: string;
  domain: string;
  status: string;
  updated_at: string;
};

export type ReportResult = {
  artifact_path: string;
  format: 'pdf' | 'csv';
  download_url?: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';

export async function createIdea(payload: IdeaPayload): Promise<IdeaAnalysisResponse> {
  const response = await fetch(`${API_BASE}/ideas`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error(`Failed to create idea: ${response.status} ${await response.text()}`);
  }
  return response.json();
}

export async function analyzeIdea(payload: IdeaPayload): Promise<IdeaAnalysisResponse> {
  const response = await fetch(`${API_BASE}/ideas/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error(`Failed to analyze idea: ${response.status} ${await response.text()}`);
  }
  return response.json();
}

export async function fetchProjects(): Promise<ProjectSummary[]> {
  const response = await fetch(`${API_BASE}/projects`, { cache: 'no-store' });
  if (!response.ok) throw new Error(`Failed to fetch projects: ${response.status}`);
  return response.json();
}

export async function generateReport(payload: { idea_id: string; format: 'pdf' | 'csv' }): Promise<ReportResult> {
  const response = await fetch(`${API_BASE}/reports`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error(`Failed to generate report: ${response.status} ${await response.text()}`);
  }
  return response.json();
}
