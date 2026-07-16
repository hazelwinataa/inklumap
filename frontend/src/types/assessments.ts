import type {
  AssessmentRecordStatus,
  AssessmentStatus,
  StudentAssessment,
} from "@/types/students";


export type AssessmentScoreField =
  | "visual_score"
  | "hearing_score"
  | "communication_score"
  | "instruction_score"
  | "attention_score"
  | "mobility_score"
  | "assistance_score"
  | "evaluation_adjustment_score";


export interface AssessmentScorePayload {
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


export interface AssessmentCreatePayload {
  student_id: number;
  assessment_date: string;
  source_information: string | null;
  notes: string | null;
  status: AssessmentRecordStatus;
  score: AssessmentScorePayload | null;
}


export interface AssessmentUpdatePayload {
  assessment_date?: string;
  source_information?: string | null;
  notes?: string | null;
  status?: AssessmentRecordStatus;
  score?: AssessmentScorePayload | null;
}


export interface AssessmentMutationResponse {
  assessment: StudentAssessment;
  student_assessment_status: AssessmentStatus;
  analytics_invalidated: boolean;
}


export interface AssessmentApiResult {
  data: AssessmentMutationResponse | null;
  error: string | null;
}