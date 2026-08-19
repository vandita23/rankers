import { Sprout, User } from "lucide-react";
import { Link } from "react-router-dom";
import { useApp } from "../../context/AppContext";
import { LANGUAGES } from "../../data/i18n";

export default function TopBar() {
  const { lang, setLang, t } = useApp();

  return (
    <header className="sticky top-0 z-30 bg-soil-50/95 backdrop-blur border-b border-soil-200">
      <div className="max-w-md mx-auto flex items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2">
          <span className="grid place-items-center w-9 h-9 rounded-xl bg-leaf-800 text-white">
            <Sprout size={20} strokeWidth={2.25} />
          </span>
          <span className="font-display font-bold text-leaf-900 text-lg leading-none">
            {t("appName")}
          </span>
        </Link>

        <div className="flex items-center gap-2">
          <div className="flex rounded-full bg-soil-100 p-1">
            {LANGUAGES.map((l) => (
              <button
                key={l.code}
                onClick={() => setLang(l.code)}
                className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                  lang === l.code
                    ? "bg-leaf-800 text-white"
                    : "text-ink-600 hover:text-leaf-800"
                }`}
                aria-pressed={lang === l.code}
              >
                {l.label}
              </button>
            ))}
          </div>
          <Link
            to="/profile"
            className="grid place-items-center w-9 h-9 rounded-full bg-leaf-100 text-leaf-800 shrink-0"
            aria-label={t("nav_profile")}
          >
            <User size={18} strokeWidth={2.25} />
          </Link>
        </div>
      </div>
    </header>
  );
}
