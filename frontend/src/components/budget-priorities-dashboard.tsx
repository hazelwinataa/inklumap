"use client";

import {
  AlertTriangle,
  BarChart3,
  Calculator,
  CheckCircle2,
  Gauge,
  RotateCcw,
  Target,
  Users,
  WalletCards,
} from "lucide-react";
import {
  useMemo,
  useState,
  type ReactNode,
} from "react";

import type {
  BudgetPriorityItem,
  BudgetPriorityResponse,
  UrgencyLevel,
} from "@/types/analytics";


interface BudgetPrioritiesDashboardProps {
  data: BudgetPriorityResponse;
}


type UrgencyFilter =
  | UrgencyLevel
  | "all";


type SortMode =
  | "priority"
  | "urgency";


export default function BudgetPrioritiesDashboard({
  data,
}: BudgetPrioritiesDashboardProps) {
  const [
    urgencyFilter,
    setUrgencyFilter,
  ] = useState<UrgencyFilter>("all");

  const [
    sortMode,
    setSortMode,
  ] = useState<SortMode>("priority");

  const highestPriority =
    data.items.reduce(
      (
        currentHighest,
        item,
      ) => (
        item.priority_points
        > currentHighest.priority_points
          ? item
          : currentHighest
      ),
      data.items[0],
    );

  const highestUrgency =
    data.items.reduce(
      (
        currentHighest,
        item,
      ) => (
        item.urgency_index
        > currentHighest.urgency_index
          ? item
          : currentHighest
      ),
      data.items[0],
    );

  const highUrgencyCount =
    data.items.filter(
      (item) =>
        item.urgency_level === "high",
    ).length;

  const displayedItems = useMemo(
    () => {
      const filtered = data.items.filter(
        (item) =>
          urgencyFilter === "all"
          || item.urgency_level
            === urgencyFilter,
      );

      return [...filtered].sort(
        (firstItem, secondItem) => {
          if (sortMode === "urgency") {
            return (
              secondItem.urgency_index
              - firstItem.urgency_index
            );
          }

          return (
            firstItem.rank
            - secondItem.rank
          );
        },
      );
    },
    [
      data.items,
      sortMode,
      urgencyFilter,
    ],
  );


  function resetControls() {
    setUrgencyFilter("all");
    setSortMode("priority");
  }


  return (
    <div className="space-y-8">
      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          title="Total Poin Prioritas"
          value={data.total_priority_points}
          description="Akumulasi skor seluruh kelompok"
          icon={
            <WalletCards size={22} />
          }
        />

        <SummaryCard
          title="Siswa Dianalisis"
          value={data.total_students}
          description="Hasil analytics pada model aktif"
          icon={
            <Users size={22} />
          }
        />

        <SummaryCard
          title="Poin Terbesar"
          value={highestPriority.priority_points}
          description={
            `Kelompok ${highestPriority.cluster_number}`
          }
          icon={
            <Target size={22} />
          }
        />

        <SummaryCard
          title="Urgensi Tertinggi"
          value={
            highestUrgency.urgency_index.toFixed(2)
          }
          description={
            `Kelompok ${highestUrgency.cluster_number}`
          }
          icon={
            <Gauge size={22} />
          }
        />
      </section>

      <section className="grid gap-5 xl:grid-cols-[1.3fr_1fr]">
        <article className="rounded-2xl border border-blue-200 bg-blue-50 p-6">
          <div className="flex gap-4">
            <div className="rounded-xl bg-white p-3 text-blue-700">
              <Calculator size={22} />
            </div>

            <div>
              <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">
                Metodologi
              </p>

              <h2 className="mt-1 text-lg font-bold text-blue-950">
                Skor prioritas berbasis kebutuhan
              </h2>

              <p className="mt-3 text-sm leading-6 text-blue-900">
                {data.methodology}
              </p>
            </div>
          </div>
        </article>

        <article className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <div className="flex gap-4">
            <div className="rounded-xl bg-white p-3 text-amber-700">
              <AlertTriangle size={22} />
            </div>

            <div>
              <p className="text-sm font-semibold uppercase tracking-wider text-amber-700">
                Catatan Penggunaan
              </p>

              <h2 className="mt-1 text-lg font-bold text-amber-950">
                Bukan nominal rupiah
              </h2>

              <p className="mt-3 text-sm leading-6 text-amber-900">
                {data.budget_note}
              </p>
            </div>
          </div>
        </article>
      </section>

      <section>
        <div className="mb-5">
          <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">
            Tiga Prioritas Utama
          </p>

          <h2 className="mt-1 text-xl font-bold text-slate-900">
            Fokus Awal Perencanaan Sumber Daya
          </h2>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            Peringkat menunjukkan besarnya kebutuhan
            secara keseluruhan. Indeks urgensi
            menunjukkan seberapa mendesak kebutuhan
            di dalam kelompok tersebut.
          </p>
        </div>

        <div className="grid gap-5 xl:grid-cols-3">
          {data.items
            .slice(0, 3)
            .map((item) => (
              <TopPriorityCard
                key={item.cluster_number}
                item={item}
              />
            ))}
        </div>
      </section>

      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-5 xl:flex-row xl:items-end xl:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">
              Kontrol Tampilan
            </p>

            <h2 className="mt-1 text-lg font-bold text-slate-900">
              Urutkan dan saring prioritas
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Terdapat {highUrgencyCount} kelompok
              dengan tingkat urgensi tinggi.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-[220px_220px_auto]">
            <div>
              <label
                htmlFor="budget-urgency-filter"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Tingkat urgensi
              </label>

              <select
                id="budget-urgency-filter"
                value={urgencyFilter}
                onChange={(event) => {
                  const value =
                    event.target.value;

                  if (
                    value === "all"
                    || value === "high"
                    || value === "medium"
                    || value === "low"
                  ) {
                    setUrgencyFilter(value);
                  }
                }}
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
              >
                <option value="all">
                  Semua urgensi
                </option>

                <option value="high">
                  Tinggi
                </option>

                <option value="medium">
                  Sedang
                </option>

                <option value="low">
                  Rendah
                </option>
              </select>
            </div>

            <div>
              <label
                htmlFor="budget-sort-mode"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Urutkan berdasarkan
              </label>

              <select
                id="budget-sort-mode"
                value={sortMode}
                onChange={(event) => {
                  const value =
                    event.target.value;

                  if (
                    value === "priority"
                    || value === "urgency"
                  ) {
                    setSortMode(value);
                  }
                }}
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
              >
                <option value="priority">
                  Peringkat prioritas
                </option>

                <option value="urgency">
                  Indeks urgensi
                </option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                type="button"
                onClick={resetControls}
                className="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-xl border border-slate-300 px-4 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 xl:w-auto"
              >
                <RotateCcw size={18} />

                Reset
              </button>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="mb-5">
          <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">
            Ranking Lengkap
          </p>

          <h2 className="mt-1 text-xl font-bold text-slate-900">
            Prioritas Kebutuhan Sumber Daya
          </h2>
        </div>

        <div className="space-y-5">
          {displayedItems.map((item) => (
            <PriorityDetailCard
              key={item.cluster_number}
              item={item}
              totalPriorityPoints={
                data.total_priority_points
              }
            />
          ))}
        </div>

        {displayedItems.length === 0 && (
          <div className="rounded-2xl border border-slate-200 bg-white px-5 py-12 text-center shadow-sm">
            <p className="font-medium text-slate-700">
              Kelompok tidak ditemukan
            </p>

            <p className="mt-1 text-sm text-slate-500">
              Ubah filter urgensi atau tekan Reset.
            </p>
          </div>
        )}
      </section>
    </div>
  );
}


interface SummaryCardProps {
  title: string;
  value: number | string;
  description: string;
  icon: ReactNode;
}


function SummaryCard({
  title,
  value,
  description,
  icon,
}: SummaryCardProps) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-600">
            {title}
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-900">
            {value}
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            {description}
          </p>
        </div>

        <div className="rounded-xl bg-blue-50 p-3 text-blue-700">
          {icon}
        </div>
      </div>
    </article>
  );
}


interface TopPriorityCardProps {
  item: BudgetPriorityItem;
}


function TopPriorityCard({
  item,
}: TopPriorityCardProps) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-lg font-bold text-white">
          {item.rank}
        </div>

        <UrgencyBadge
          urgency={item.urgency_level}
        />
      </div>

      <p className="mt-5 text-sm font-semibold uppercase tracking-wider text-blue-700">
        Kelompok {item.cluster_number}
      </p>

      <h3 className="mt-2 text-lg font-bold text-slate-900">
        {item.cluster_name}
      </h3>

      <p className="mt-3 text-sm leading-6 text-slate-600">
        {item.dominant_need}
      </p>

      <div className="mt-5 grid grid-cols-2 gap-3">
        <MetricBox
          label="Poin"
          value={item.priority_points}
        />

        <MetricBox
          label="Proporsi"
          value={
            `${item.priority_share_percentage}%`
          }
        />

        <MetricBox
          label="Urgensi"
          value={item.urgency_index.toFixed(2)}
        />

        <MetricBox
          label="Siswa"
          value={item.total_students}
        />
      </div>
    </article>
  );
}


interface PriorityDetailCardProps {
  item: BudgetPriorityItem;
  totalPriorityPoints: number;
}


function PriorityDetailCard({
  item,
  totalPriorityPoints,
}: PriorityDetailCardProps) {
  const calculatedShare =
    totalPriorityPoints > 0
      ? (
        item.priority_points
        / totalPriorityPoints
      ) * 100
      : 0;

  return (
    <article className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 p-6">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div className="flex gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-lg font-bold text-white">
              {item.rank}
            </div>

            <div>
              <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">
                Kelompok {item.cluster_number}
              </p>

              <h3 className="mt-1 text-xl font-bold text-slate-900">
                {item.cluster_name}
              </h3>

              <p className="mt-2 text-sm font-medium text-slate-600">
                Kebutuhan dominan:{" "}
                {item.dominant_need}
              </p>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            <span className="inline-flex rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-sm font-bold text-blue-700">
              {item.priority_points} poin
            </span>

            <UrgencyBadge
              urgency={item.urgency_level}
            />
          </div>
        </div>

        <p className="mt-5 max-w-4xl text-sm leading-6 text-slate-600">
          {item.description}
        </p>
      </div>

      <div className="grid gap-6 p-6 xl:grid-cols-[1fr_1.2fr]">
        <div className="space-y-5">
          <section>
            <div className="mb-2 flex items-center justify-between gap-4 text-sm">
              <span className="font-medium text-slate-700">
                Proporsi total prioritas
              </span>

              <span className="font-bold text-slate-900">
                {item.priority_share_percentage}%
              </span>
            </div>

            <div className="h-3 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-blue-600"
                style={{
                  width: `${Math.min(
                    calculatedShare,
                    100,
                  )}%`,
                }}
              />
            </div>
          </section>

          <section>
            <div className="mb-2 flex items-center justify-between gap-4 text-sm">
              <span className="font-medium text-slate-700">
                Indeks urgensi
              </span>

              <span className="font-bold text-slate-900">
                {item.urgency_index.toFixed(2)}
              </span>
            </div>

            <div className="h-3 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-amber-500"
                style={{
                  width: `${Math.min(
                    item.urgency_index,
                    100,
                  )}%`,
                }}
              />
            </div>
          </section>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            <MetricBox
              label="Prioritas tinggi"
              value={item.high_priority}
            />

            <MetricBox
              label="Prioritas sedang"
              value={item.medium_priority}
            />

            <MetricBox
              label="Prioritas rendah"
              value={item.low_priority}
            />

            <MetricBox
              label="Akses kritis"
              value={item.critical_access}
            />

            <MetricBox
              label="Perlu validasi"
              value={item.needs_human_review}
            />

            <MetricBox
              label="Total siswa"
              value={item.total_students}
            />
          </div>

          <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
            <div className="flex gap-3">
              <BarChart3
                size={19}
                className="mt-0.5 shrink-0 text-blue-700"
              />

              <p className="text-sm leading-6 text-slate-700">
                {item.rationale}
              </p>
            </div>
          </div>
        </div>

        <section>
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-emerald-50 p-3 text-emerald-700">
              <CheckCircle2 size={20} />
            </div>

            <div>
              <p className="text-sm font-semibold uppercase tracking-wider text-emerald-700">
                Tindakan Direkomendasikan
              </p>

              <h4 className="mt-1 font-bold text-slate-900">
                Arah penggunaan sumber daya
              </h4>
            </div>
          </div>

          <ul className="mt-5 space-y-3">
            {item.recommended_actions.map(
              (action) => (
                <li
                  key={action}
                  className="flex gap-3 rounded-xl border border-emerald-100 bg-emerald-50/60 p-4 text-sm leading-6 text-slate-700"
                >
                  <CheckCircle2
                    size={18}
                    className="mt-1 shrink-0 text-emerald-600"
                  />

                  <span>
                    {action}
                  </span>
                </li>
              ),
            )}
          </ul>
        </section>
      </div>
    </article>
  );
}


interface MetricBoxProps {
  label: string;
  value: number | string;
}


function MetricBox({
  label,
  value,
}: MetricBoxProps) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
      <p className="text-xs leading-5 text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-lg font-bold text-slate-900">
        {value}
      </p>
    </div>
  );
}


interface UrgencyBadgeProps {
  urgency: UrgencyLevel;
}


function UrgencyBadge({
  urgency,
}: UrgencyBadgeProps) {
  let label = "Rendah";
  let className = (
    "border-emerald-200 "
    + "bg-emerald-50 "
    + "text-emerald-700"
  );

  if (urgency === "high") {
    label = "Urgensi tinggi";
    className = (
      "border-red-200 "
      + "bg-red-50 "
      + "text-red-700"
    );
  }

  if (urgency === "medium") {
    label = "Urgensi sedang";
    className = (
      "border-amber-200 "
      + "bg-amber-50 "
      + "text-amber-700"
    );
  }

  return (
    <span
      className={[
        "inline-flex rounded-full border px-3 py-1 text-xs font-semibold",
        className,
      ].join(" ")}
    >
      {label}
    </span>
  );
}
