
import type {
  AnalyticsStudentDetail,
  AnalyticsStudentListResponse,
  AnalyticsSummary,
  BudgetPriorityResponse,
  ClusterProfile,
  GetAnalyticsStudentsParams,
} from "@/types/analytics";
import type {
  AssessmentApiResult,
  AssessmentCreatePayload,
  AssessmentUpdatePayload,
} from "@/types/assessments";
import type {
  GetStudentsParams,
  StudentDetail,
  StudentListResponse,
  StudentSummary,
} from "@/types/students";


const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000";


async function getApiErrorMessage(
  response: Response,
): Promise<string> {
  try {
    const responseData = await response.json();

    if (
      typeof responseData?.detail === "string"
    ) {
      return responseData.detail;
    }

    if (Array.isArray(responseData?.detail)) {
      const messages = responseData.detail
        .map((item: unknown) => {
          if (
            typeof item === "object"
            && item !== null
            && "msg" in item
            && typeof item.msg === "string"
          ) {
            return item.msg;
          }

          return null;
        })
        .filter(
          (message: string | null):
            message is string => message !== null,
        );

      if (messages.length > 0) {
        return messages.join(" ");
      }
    }
  } catch {
    // Respons error tidak selalu berbentuk JSON.
  }

  return (
    "Permintaan gagal dengan status "
    + `${response.status}.`
  );
}


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


export async function getBudgetPriorities():
  Promise<BudgetPriorityResponse | null> {
  try {
    const response = await fetch(
      (
        `${API_URL}/api/analytics/`
        + "budget-priorities"
      ),
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


export async function getClusterProfiles():
  Promise<ClusterProfile[] | null> {
  try {
    const response = await fetch(
      `${API_URL}/api/analytics/clusters`,
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


export async function getAnalyticsStudents({
  skip = 0,
  limit = 100,
}: GetAnalyticsStudentsParams = {}):
  Promise<AnalyticsStudentListResponse | null> {
  try {
    const url = new URL(
      `${API_URL}/api/analytics/students`,
    );

    url.searchParams.set(
      "skip",
      String(skip),
    );

    url.searchParams.set(
      "limit",
      String(limit),
    );

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
        "status",
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


export async function createAssessment(
  payload: AssessmentCreatePayload,
): Promise<AssessmentApiResult> {
  try {
    const response = await fetch(
      `${API_URL}/api/assessments`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        cache: "no-store",
      },
    );

    if (!response.ok) {
      return {
        data: null,
        error: await getApiErrorMessage(
          response,
        ),
      };
    }

    return {
      data: await response.json(),
      error: null,
    };
  } catch {
    return {
      data: null,
      error: (
        "Backend tidak dapat dihubungi. "
        + "Pastikan FastAPI masih berjalan."
      ),
    };
  }
}


export async function updateAssessment(
  assessmentId: number,
  payload: AssessmentUpdatePayload,
): Promise<AssessmentApiResult> {
  try {
    const response = await fetch(
      (
        `${API_URL}/api/assessments/`
        + assessmentId
      ),
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        cache: "no-store",
      },
    );

    if (!response.ok) {
      return {
        data: null,
        error: await getApiErrorMessage(
          response,
        ),
      };
    }

    return {
      data: await response.json(),
      error: null,
    };
  } catch {
    return {
      data: null,
      error: (
        "Backend tidak dapat dihubungi. "
        + "Pastikan FastAPI masih berjalan."
      ),
    };
  }
}
