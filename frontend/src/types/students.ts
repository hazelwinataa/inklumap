export type AssessmentStatus =
  | "complete"
  | "incomplete"
  | "not_started";


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