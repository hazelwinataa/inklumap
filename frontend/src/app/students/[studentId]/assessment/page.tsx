import {
  notFound,
} from "next/navigation";

import AssessmentForm from "@/components/assessment-form";
import {
  getStudentDetail,
} from "@/lib/api";


interface AssessmentPageProps {
  params: Promise<{
    studentId: string;
  }>;
}


export default async function AssessmentPage({
  params,
}: AssessmentPageProps) {
  const {
    studentId,
  } = await params;

  const parsedStudentId =
    Number(studentId);

  if (
    !Number.isInteger(parsedStudentId)
    || parsedStudentId <= 0
  ) {
    notFound();
  }

  const student = await getStudentDetail(
    parsedStudentId,
  );

  if (!student) {
    notFound();
  }

  const latestAssessment = [
    ...student.assessments,
  ].sort(
    (
      firstAssessment,
      secondAssessment,
    ) => {
      const dateComparison =
        secondAssessment.assessment_date
          .localeCompare(
            firstAssessment.assessment_date,
          );

      if (dateComparison !== 0) {
        return dateComparison;
      }

      return (
        secondAssessment.id
        - firstAssessment.id
      );
    },
  )[0] ?? null;

  return (
    <AssessmentForm
      student={student}
      initialAssessment={
        latestAssessment
      }
    />
  );
}