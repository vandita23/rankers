import { createContext, useContext, useState, useMemo, useEffect, useCallback } from "react";
import { dict } from "../data/i18n";
import { getDashboard } from "../lib/api";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [lang, setLang] = useState("en");
  const [dashboard, setDashboard] = useState(null);
  const [dashboardLoading, setDashboardLoading] = useState(true);
  const [dashboardError, setDashboardError] = useState(null);

  const t = useMemo(() => {
    const strings = dict[lang];
    return (key) => strings[key] ?? key;
  }, [lang]);

  const loadDashboard = useCallback(async (language) => {
    setDashboardLoading(true);
    setDashboardError(null);
    try {
      const data = await getDashboard(language);
      setDashboard(data);
    } catch (err) {
      setDashboardError(err.message ?? "Failed to load dashboard");
    } finally {
      setDashboardLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboard(lang);
  }, [lang, loadDashboard]);

  const value = {
    lang,
    setLang,
    t,
    dashboard,
    dashboardLoading,
    dashboardError,
    refreshDashboard: () => loadDashboard(lang),
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used within AppProvider");
  return ctx;
}
