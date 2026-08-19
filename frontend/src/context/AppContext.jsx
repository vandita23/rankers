import { createContext, useContext, useState, useMemo } from "react";
import { dict } from "../data/i18n";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [lang, setLang] = useState("en");

  const t = useMemo(() => {
    const strings = dict[lang];
    return (key) => strings[key] ?? key;
  }, [lang]);

  const value = { lang, setLang, t };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used within AppProvider");
  return ctx;
}
