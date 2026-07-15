import type {
  AnalyticsSummary,
} from "@/types/analytics";


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