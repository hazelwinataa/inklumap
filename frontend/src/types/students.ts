export type AssessmentStatus =
  | "complete"
  | "incomplete"
  | "not_started";

export type AssessmentRecordStatus =
  | "draft"
  | "submitted"
  | "validated";


export interface StudentListItem {
  id: number;
  student_code: string;
  initials: string | null;
  grade_level: string | null;
  class_name: string | null;
  semester: string | null;
  school_year: string | null;
  assessment_status: AssessmentStatus;
  created_at: string;
  updated_at: string;
}


export interface StudentListResponse {
  total: number;
  skip: number;
  limit: number;
  items: StudentListItem[];
}


export interface StudentSummary {
  total_students: number;
  complete: number;
  incomplete: number;
  not_started: number;
  total_assessments: number;
  total_scores: number;
}


export interface GetStudentsParams {
  skip?: number;
  limit?: number;
  search?: string;
  assessmentStatus?: AssessmentStatus;
}


export interface AssessmentScore {
  id: number;
  assessment_id: number;

  visual_score: number | null;
  hearing_score: number | null;
  communication_score: number | null;
  instruction_score: number | null;
  attention_score: number | null;
  mobility_score: number | null;
  assistance_score: number | null;
  evaluation_adjustment_score: number | null;

  material_preferences: string[];
  assistive_tools: string[];
}


export interface StudentAssessment {
  id: number;
  student_id: number;
  assessor_id: number | null;

  assessment_date: string;
  source_information: string | null;
  notes: string | null;
  status: AssessmentRecordStatus;

  created_at: string;
  updated_at: string;

  score: AssessmentScore | null;
}


export interface StudentDetail
  extends StudentListItem {
  assessments: StudentAssessment[];
}