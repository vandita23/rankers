import { useState } from "react";
import { Search, ChevronDown, FileCheck2, ListOrdered, BadgeCheck } from "lucide-react";
import { useApp } from "../context/AppContext";
import PageContainer from "../components/layout/PageContainer";
import Card from "../components/ui/Card";
import { schemes } from "../data/mock";

function SchemeCard({ scheme, lang, t }) {
  const [open, setOpen] = useState(false);

  return (
    <Card padded={false} className="overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-start justify-between gap-3 p-4 text-left"
      >
        <div>
          <h3 className="font-display font-bold text-leaf-900 text-[15px] leading-snug">
            {lang === "hi" ? scheme.name_hi : scheme.name_en}
          </h3>
          <p className="text-ink-600 text-sm mt-1 leading-snug">
            {lang === "hi" ? scheme.summary_hi : scheme.summary_en}
          </p>
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
              {(lang === "hi" ? scheme.eligibility_hi : scheme.eligibility_en).map((e, i) => (
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
              {(lang === "hi" ? scheme.documents_hi : scheme.documents_en).map((d, i) => (
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
              {(lang === "hi" ? scheme.steps_hi : scheme.steps_en).map((s, i) => (
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

  const filtered = schemes.filter((s) => {
    const name = lang === "hi" ? s.name_hi : s.name_en;
    const summary = lang === "hi" ? s.summary_hi : s.summary_en;
    const q = query.toLowerCase();
    return !q || name.toLowerCase().includes(q) || summary.toLowerCase().includes(q);
  });

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
      </div>

      <div className="space-y-3">
        {filtered.map((s) => (
          <SchemeCard key={s.id} scheme={s} lang={lang} t={t} />
        ))}
      </div>
    </PageContainer>
  );
}
