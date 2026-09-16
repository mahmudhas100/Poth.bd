import type { Metadata, Viewport } from "next";
import { Hind_Siliguri, Outfit } from "next/font/google";
import "./globals.css";

const hindSiliguri = Hind_Siliguri({
  subsets: ["bengali"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-bengali",
});

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-display",
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


export const viewport: Viewport = {
  themeColor: "#2563eb",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="bn" className={`${hindSiliguri.variable} ${outfit.variable}`}>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
                  navigator.serviceWorker.getRegistrations().then(function(registrations) {
                    for(let registration of registrations) {
                      registration.unregister();
                    }
                  });
                } else {
                  window.addEventListener('load', function() {
                    navigator.serviceWorker.register('/sw.js').catch(function(err) {
                      console.log('ServiceWorker registration failed: ', err);
                    });
                  });
                }
              }
            `,
          }}
        />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
