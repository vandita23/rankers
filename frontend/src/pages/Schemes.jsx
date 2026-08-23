import { useEffect, useState } from "react";
import { Search, ChevronDown, FileCheck2, ListOrdered, BadgeCheck, Loader2 } from "lucide-react";
import { useApp } from "../context/AppContext";
import PageContainer from "../components/layout/PageContainer";
import Card from "../components/ui/Card";
import { queryScheme } from "../lib/api";

const DEFAULT_QUESTION = "What government schemes are available for farmers?";
const DEBOUNCE_MS = 450;

function SchemeCard({ scheme, t }) {
  const [open, setOpen] = useState(false);

  return (
    <Card padded={false} className="overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-start justify-between gap-3 p-4 text-left"
      >
        <div>
          <h3 className="font-display font-bold text-leaf-900 text-[15px] leading-snug">
            {scheme.name}
          </h3>
          <p className="text-ink-600 text-sm mt-1 leading-snug">{scheme.summary}</p>
        </div>
        <ChevronDown
          size={20}
          className={`shrink-0 text-leaf-800 mt-1 transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>

      {open && (
        <div className="px-4 pb-4 space-y-4 border-t border-soil-200 pt-4">
          <div>
            <p className="flex items-center gap-1.5 text-xs font-bold text-leaf-800 uppercase tracking-wide mb-2">
              <BadgeCheck size={14} /> {t("schemes_eligibility")}
            </p>
            <ul className="space-y-1.5">
              {(scheme.eligibility ?? []).map((e, i) => (
                <li key={i} className="text-sm text-ink-900 flex gap-2">
                  <span className="text-leaf-600">•</span>
                  {e}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="flex items-center gap-1.5 text-xs font-bold text-leaf-800 uppercase tracking-wide mb-2">
              <FileCheck2 size={14} /> {t("schemes_documents")}
            </p>
            <ul className="space-y-1.5">
              {(scheme.documents ?? []).map((d, i) => (
                <li key={i} className="text-sm text-ink-900 flex gap-2">
                  <span className="text-leaf-600">•</span>
                  {d}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="flex items-center gap-1.5 text-xs font-bold text-leaf-800 uppercase tracking-wide mb-2">
              <ListOrdered size={14} /> {t("schemes_steps")}
            </p>
            <ol className="space-y-2">
              {(scheme.steps ?? []).map((s, i) => (
                <li key={i} className="flex gap-2.5 text-sm text-ink-900 leading-snug">
                  <span className="shrink-0 w-5 h-5 grid place-items-center rounded-full bg-leaf-100 text-leaf-800 text-[11px] font-bold">
                    {i + 1}
                  </span>
                  {s}
                </li>
              ))}
            </ol>
          </div>

          <p className="text-[11px] text-ink-400 pt-1">
            {t("schemes_source")}: {scheme.source}
          </p>
        </div>
      )}
    </Card>
  );
}

export default function Schemes() {
  const { t, lang } = useApp();
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const question = query.trim() || DEFAULT_QUESTION;
    const handle = setTimeout(() => {
      let cancelled = false;
      setLoading(true);
      setError(null);

      queryScheme(question, lang)
        .then((data) => {
          if (cancelled) return;
          setAnswer(data.answer);
          setSchemes(Array.isArray(data.schemes) ? data.schemes : []);
        })
        .catch((err) => {
          if (!cancelled) setError(err.message ?? "Failed to load schemes");
        })
        .finally(() => {
          if (!cancelled) setLoading(false);
        });

      return () => {
        cancelled = true;
      };
    }, query ? DEBOUNCE_MS : 0);

    return () => clearTimeout(handle);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query, lang]);

  return (
    <PageContainer>
      <div className="mb-4">
        <h1 className="font-display text-xl font-extrabold text-leaf-900">{t("schemes_title")}</h1>
        <p className="text-ink-600 text-sm mt-1">{t("schemes_subtitle")}</p>
      </div>

      <div className="flex items-center gap-2.5 bg-white border border-soil-200 rounded-xl px-3.5 py-3 mb-4">
        <Search size={18} className="text-ink-400 shrink-0" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t("schemes_searchPlaceholder")}
          className="flex-1 outline-none text-sm bg-transparent placeholder:text-ink-400"
        />
        {loading && <Loader2 size={16} className="animate-spin text-ink-400 shrink-0" />}
      </div>

      {answer && !loading && (
        <Card className="mb-4 bg-leaf-100/50 border-leaf-400/30 text-sm text-ink-900">{answer}</Card>
      )}

      {error && (
        <Card className="mb-4 border-clay-500/40 bg-marigold-100 text-sm text-ink-900">{error}</Card>
      )}

      {loading && schemes.length === 0 ? (
        <Card className="flex items-center justify-center py-10 text-ink-400">
          <Loader2 size={22} className="animate-spin" />
        </Card>
      ) : (
        <div className="space-y-3">
          {schemes.map((s) => (
            <SchemeCard key={s.name} scheme={s} t={t} />
          ))}
        </div>
      )}
    </PageContainer>
  );
}
