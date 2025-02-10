import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";

import Navbar from "@/components/Navbar/Navbar";

export const metadata: Metadata = {
  title: "SAMAY - Your Spiritual Guide",
  description: "Explore spiritual wisdom through modern conversation",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-gray-50">
       <Navbar/>
       <div className="mt-8 py-8 mb-16">
        <Providers>{children}</Providers>
       </div>
      </body>
    </html>
  );
}
