import type {
  Metadata,
} from "next";
import {
  Geist,
  Geist_Mono,
} from "next/font/google";

import DashboardLayout from "@/components/dashboard-layout";

import "./globals.css";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});


export const metadata: Metadata = {
  title: {
    default: "InkluMap",
    template: "%s | InkluMap",
  },
  description: (
    "Sistem pemetaan kebutuhan akomodasi "
    + "pembelajaran sekolah inklusif."
  ),
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body
        className={[
          geistSans.variable,
          geistMono.variable,
          "antialiased",
        ].join(" ")}
      >
        <DashboardLayout>
          {children}
        </DashboardLayout>
      </body>
    </html>
  );
}