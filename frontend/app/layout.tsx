import type { Metadata } from "next";
import { Nunito } from "next/font/google";
import "./globals.css";
import { UserProvider } from "@/lib/user-context";
import { ApiBootstrap } from "@/lib/api-bootstrap";

const nunito = Nunito({
  subsets: ["latin"],
  weight: ["600", "700", "800", "900"],
});

export const metadata: Metadata = {
  title: "Fluent — Learn Spanish",
  description: "A Duolingo-style language learning app.",
};

const themeScript = `
(function() {
  try {
    var theme = localStorage.getItem("fluent-theme") || localStorage.getItem("lingo-theme");
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    }
  } catch (error) {}
})();
`;

function readApiUrl() {
  const fromPublic = process.env.NEXT_PUBLIC_API_URL || "";
  if (fromPublic !== "") {
    return fromPublic;
  }
  return process.env.API_PUBLIC_URL || "";
}

export default function RootLayout({ children }: LayoutProps<"/">) {
  const apiUrl = readApiUrl();

  return (
    <html lang="en">
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className={nunito.className}>
        <ApiBootstrap apiUrl={apiUrl}>
          <UserProvider>{children}</UserProvider>
        </ApiBootstrap>
      </body>
    </html>
  );
}
