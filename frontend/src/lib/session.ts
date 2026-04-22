import type { IdeaPayload, IdeaAnalysisResponse } from "./api";

const IDEA_PAYLOAD_KEY = "iic:last-idea-payload";
const IDEA_RESULT_KEY = "iic:last-idea-result";

export function saveIdeaPayload(payload: IdeaPayload) {
  if (typeof window === "undefined") return;
  window.sessionStorage.setItem(IDEA_PAYLOAD_KEY, JSON.stringify(payload));
}

export function loadIdeaPayload(): IdeaPayload | null {
  if (typeof window === "undefined") return null;
  const raw = window.sessionStorage.getItem(IDEA_PAYLOAD_KEY);
  if (!raw) return null;

  try {
    return JSON.parse(raw) as IdeaPayload;
  } catch {
    return null;
  }
}

export function saveIdeaResult(result: IdeaAnalysisResponse) {
  if (typeof window === "undefined") return;
  window.sessionStorage.setItem(IDEA_RESULT_KEY, JSON.stringify(result));
}

export function loadIdeaResult(): IdeaAnalysisResponse | null {
  if (typeof window === "undefined") return null;
  const raw = window.sessionStorage.getItem(IDEA_RESULT_KEY);
  if (!raw) return null;

  try {
    return JSON.parse(raw) as IdeaAnalysisResponse;
  } catch {
    return null;
  }
}

export function clearIdeaSession() {
  if (typeof window === "undefined") return;
  window.sessionStorage.removeItem(IDEA_PAYLOAD_KEY);
  window.sessionStorage.removeItem(IDEA_RESULT_KEY);
}