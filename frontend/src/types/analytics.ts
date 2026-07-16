export type PriorityLevel =
  | "high"
  | "medium"
  | "low";


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


export interface AnalyticsStudentDetail {
  student_id: number;
  student_code: string;
  initials: string | null;
  grade_level: string | null;
  class_name: string | null;

  assessment_id: number;
  cluster_result_id: number;

  cluster_number: number;
  cluster_name: string;
  priority_level: PriorityLevel;

  dominant_needs: string[];

  critical_access_flag: boolean;
  dbscan_unique_case: boolean;
  needs_human_review: boolean;

  individual_silhouette: number;
  mean_distance_to_cluster: number;

  model_version: string;

  maximum_need_score: number;
  average_need_score: number;
  critical_domain_count: number;
  high_domain_count: number;

  critical_access_domains: string[];
  human_review_reason: string | null;
  priority_action: string | null;

  cluster_recommendations: string[];
  individual_recommendations: string[];

  material_preference: string | null;
  assistive_tool: string | null;
  recommendation_status: string | null;
}