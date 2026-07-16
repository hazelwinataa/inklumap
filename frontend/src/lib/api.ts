import type {
  AnalyticsStudentDetail,
  AnalyticsSummary,
} from "@/types/analytics";
import type {
  GetStudentsParams,
  StudentDetail,
  StudentListResponse,
  StudentSummary,
} from "@/types/students";


const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000";


export async function getAnalyticsSummary():
  Promise<AnalyticsSummary | null> {
  try {
    const response = await fetch(
      `${API_URL}/api/analytics/summary`,
      {
        cache: "no-store",
      },
    );

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch {
    return null;
  }
}


export async function getStudentSummary():
  Promise<StudentSummary | null> {
  try {
    const response = await fetch(
      `${API_URL}/api/students/summary`,
      {
        cache: "no-store",
      },
    );

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch {
    return null;
  }
}


export async function getStudents({
  skip = 0,
  limit = 10,
  search,
  assessmentStatus,
}: GetStudentsParams = {}):
  Promise<StudentListResponse | null> {
  try {
    const url = new URL(
      `${API_URL}/api/students`,
    );

    url.searchParams.set(
      "skip",
      String(skip),
    );

    url.searchParams.set(
      "limit",
      String(limit),
    );

    if (search?.trim()) {
      url.searchParams.set(
        "search",
        search.trim(),
      );
    }

    if (assessmentStatus) {
      url.searchParams.set(
        "assessment_status",
        assessmentStatus,
      );
    }

    const response = await fetch(
      url.toString(),
      {
        cache: "no-store",
      },
    );

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch {
    return null;
  }
}


export async function getStudentDetail(
  studentId: number,
): Promise<StudentDetail | null> {
  try {
    const response = await fetch(
      `${API_URL}/api/students/${studentId}`,
      {
        cache: "no-store",
      },
    );

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch {
    return null;
  }
}


export async function getAnalyticsStudentDetail(
  studentId: number,
): Promise<AnalyticsStudentDetail | null> {
  try {
    const response = await fetch(
      `${API_URL}/api/analytics/students/${studentId}`,
      {
        cache: "no-store",
      },
    );

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch {
    return null;
  }
}