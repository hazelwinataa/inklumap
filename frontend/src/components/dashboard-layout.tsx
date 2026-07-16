
"use client";

import {
  Accessibility,
  ChartNoAxesCombined,
  FileText,
  LayoutDashboard,
  Menu,
  Network,
  Users,
  WalletCards,
  X,
} from "lucide-react";
import Link from "next/link";
import {
  usePathname,
} from "next/navigation";
import {
  useState,
  type ReactNode,
} from "react";


interface DashboardLayoutProps {
  children: ReactNode;
}


const navigationItems = [
  {
    label: "Ringkasan",
    href: "/",
    icon: LayoutDashboard,
  },
  {
    label: "Data Siswa",
    href: "/students",
    icon: Users,
  },
  {
    label: "Kelompok Kebutuhan",
    href: "/clusters",
    icon: Network,
  },
  {
    label: "Rekomendasi",
    href: "/recommendations",
    icon: ChartNoAxesCombined,
  },
  {
    label: "Prioritas Anggaran",
    href: "/budget-priorities",
    icon: WalletCards,
  },
  {
    label: "Laporan",
    href: "/reports",
    icon: FileText,
  },
];


export default function DashboardLayout({
  children,
}: DashboardLayoutProps) {
  const pathname = usePathname();

  const [
    mobileMenuOpen,
    setMobileMenuOpen,
  ] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-72 flex-col border-r border-slate-800 bg-slate-950 lg:flex">
        <SidebarContent
          pathname={pathname}
          closeMenu={() => {
            setMobileMenuOpen(false);
          }}
        />
      </aside>

      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <button
            type="button"
            aria-label="Tutup menu navigasi"
            className="absolute inset-0 bg-slate-950/60"
            onClick={() => {
              setMobileMenuOpen(false);
            }}
          />

          <aside className="relative h-full w-72 border-r border-slate-800 bg-slate-950 shadow-2xl">
            <button
              type="button"
              aria-label="Tutup menu"
              className="absolute right-4 top-4 rounded-lg p-2 text-slate-300 hover:bg-slate-800 hover:text-white"
              onClick={() => {
                setMobileMenuOpen(false);
              }}
            >
              <X size={21} />
            </button>

            <SidebarContent
              pathname={pathname}
              closeMenu={() => {
                setMobileMenuOpen(false);
              }}
            />
          </aside>
        </div>
      )}

      <div className="lg:pl-72">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-4 backdrop-blur sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <button
              type="button"
              aria-label="Buka menu navigasi"
              className="rounded-lg border border-slate-200 p-2 text-slate-700 hover:bg-slate-100 lg:hidden"
              onClick={() => {
                setMobileMenuOpen(true);
              }}
            >
              <Menu size={21} />
            </button>

            <div>
              <p className="text-sm font-semibold text-slate-900">
                Dashboard InkluMap
              </p>

              <p className="hidden text-xs text-slate-500 sm:block">
                Pemetaan kebutuhan akomodasi pembelajaran
              </p>
            </div>
          </div>

          <div className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700">
            Sistem aktif
          </div>
        </header>

        <main>
          {children}
        </main>
      </div>
    </div>
  );
}


interface SidebarContentProps {
  pathname: string;
  closeMenu: () => void;
}


function SidebarContent({
  pathname,
  closeMenu,
}: SidebarContentProps) {
  return (
    <>
      <div className="flex h-24 items-center gap-3 border-b border-slate-800 px-6">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-white">
          <Accessibility size={25} />
        </div>

        <div>
          <p className="text-xl font-bold tracking-tight text-white">
            InkluMap
          </p>

          <p className="text-xs text-slate-400">
            Sekolah Inklusif
          </p>
        </div>
      </div>

      <nav
        aria-label="Navigasi utama"
        className="flex-1 space-y-1 px-4 py-6"
      >
        {navigationItems.map((item) => {
          const Icon = item.icon;

          const isActive =
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(
                  item.href,
                );

          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={closeMenu}
              className={[
                "flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition",
                isActive
                  ? "bg-blue-600 text-white shadow-lg shadow-blue-950/20"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white",
              ].join(" ")}
            >
              <Icon size={20} />

              <span>
                {item.label}
              </span>
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-slate-800 p-5">
        <div className="rounded-xl bg-slate-900 p-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Model aktif
          </p>

          <p className="mt-2 text-sm font-semibold text-white">
            Hierarchical Gower
          </p>

          <p className="mt-1 text-xs text-slate-400">
            Silhouette Score 0.6757
          </p>
        </div>
      </div>
    </>
  );
}
