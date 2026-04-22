import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Intelligent Innovation Copilot",
  description: "AI-powered innovation analysis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full bg-slate-950 text-slate-100 antialiased">
        {children}
      </body>
    </html>
  );
}