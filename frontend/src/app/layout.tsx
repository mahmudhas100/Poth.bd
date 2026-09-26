import type { Metadata, Viewport } from "next";
import { Hind_Siliguri, Outfit } from "next/font/google";
import "./globals.css";

const hindSiliguri = Hind_Siliguri({
  subsets: ["bengali"],
  weight: ["400", "600", "700"],
  display: "swap",
  variable: "--font-bengali",
  preload: true,
});

const outfit = Outfit({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-display",
  preload: true,
});

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://poth.bd";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Poth.bd (পথ) — সঠিক রুট, নির্ভুল ভাড়া",
    template: "%s | Poth.bd",
  },
  description: "ঢাকা শহরের বাস রুট ও বিআরটিএ অনুমোদিত সঠিক ভাড়ার আধুনিক ডিজিটাল নেভিগেটর।",
  keywords: [
    "bus fare",
    "dhaka bus route",
    "brta bus fare",
    "বাস ভাড়া",
    "ঢাকা বাস রুট",
    "poth.bd",
    "পথ",
    "transit bangladesh",
  ],
  authors: [{ name: "Poth.bd Team" }],
  manifest: "/manifest.webmanifest",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "Poth.bd",
  },
  icons: {
    icon: "/icon-192.png",
    apple: "/apple-touch-icon.png",
  },
  openGraph: {
    type: "website",
    locale: "bn_BD",
    url: siteUrl,
    title: "Poth.bd (পথ) — সঠিক রুট, নির্ভুল ভাড়া",
    description: "ঢাকা শহরের বাস রুট ও বিআরটিএ অনুমোদিত সঠিক ভাড়ার আধুনিক ডিজিটাল নেভিগেটর।",
    siteName: "Poth.bd",
    images: [
      {
        url: "/icon-512.png",
        width: 512,
        height: 512,
        alt: "Poth.bd Logo",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Poth.bd (পথ) — সঠিক রুট, নির্ভুল ভাড়া",
    description: "ঢাকা শহরের বাস রুট ও বিআরটিএ অনুমোদিত সঠিক ভাড়ার আধুনিক ডিজিটাল নেভিগেটর।",
    images: ["/icon-512.png"],
  },
};


import { Analytics } from "@vercel/analytics/next";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { ServiceWorkerRegister } from "@/components/ServiceWorkerRegister";

export const viewport: Viewport = {
  themeColor: "#2563eb",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="bn" className={`${hindSiliguri.variable} ${outfit.variable}`}>
      <body className="antialiased">
        <ServiceWorkerRegister />
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}

