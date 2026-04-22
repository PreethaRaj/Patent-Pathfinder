import type { IdeaPayload } from "./api";

export const warehouseStockoutPayload: IdeaPayload = {
  title: "Warehouse Stockout Prediction",
  problem_statement:
    "I want an AI system that predicts warehouse stockouts using camera feeds from shelves and ERP inventory signals. The model should alert managers when a shelf is empty before the ERP catches up.",
  domain: "retail-operations",
  objectives: ["Real-time stockout prediction", "Pre-ERP alerting"],
  constraints: ["Edge deployment", "Low latency"],
  tags: ["AI", "computer-vision", "logistics"],
};
