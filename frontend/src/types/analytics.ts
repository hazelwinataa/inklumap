export interface AnalyticsSummary {
  model_version: string;
  model_name: string;
  silhouette_score: number | null;

  total_students: number;
  cluster_count: number;

  high_priority: number;
  medium_priority: number;
  low_priority: number;

  critical_access: number;
  dbscan_unique_cases: number;
  needs_human_review: number;
}