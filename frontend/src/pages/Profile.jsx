import { MapPin, Languages, Sprout, Info, User } from "lucide-react";
import { useApp } from "../context/AppContext";
import PageContainer from "../components/layout/PageContainer";
import Card from "../components/ui/Card";
import Badge from "../components/ui/Badge";
import { LANGUAGES } from "../data/i18n";

export default function Profile() {
  const { t, lang, setLang, dashboard, dashboardLoading } = useApp();
  const farmer = dashboard?.farmer;
  const name = farmer?.name ?? "—";
  const location = farmer?.location ?? "";
  const crops = farmer?.crops ?? [];

  return (
    <PageContainer>
      <h1 className="font-display text-xl font-extrabold text-leaf-900 mb-4">
        {t("profile_title")}
      </h1>

      <Card className="flex items-center gap-3.5 mb-4">
        <span className="grid place-items-center w-14 h-14 rounded-full bg-leaf-100 text-leaf-800">
          <User size={26} strokeWidth={2} />
        </span>
        <div>
          <p className="font-display font-bold text-leaf-900 text-base">
            {dashboardLoading ? t("common_loading") : name}
          </p>
          <p className="text-ink-600 text-sm">{location}</p>
        </div>
      </Card>

      <Card className="mb-4">
        <p className="flex items-center gap-2 text-xs font-bold text-leaf-800 uppercase tracking-wide mb-3">
          <Languages size={14} /> {t("profile_language")}
        </p>
        <div className="flex gap-2">
          {LANGUAGES.map((l) => (
            <button
              key={l.code}
              onClick={() => setLang(l.code)}
              className={`flex-1 rounded-xl py-2.5 text-sm font-semibold transition-colors ${
                lang === l.code
                  ? "bg-leaf-800 text-white"
                  : "bg-soil-100 text-ink-600"
              }`}
            >
              {l.label}
            </button>
          ))}
        </div>
      </Card>

      <Card className="mb-4">
        <p className="flex items-center gap-2 text-xs font-bold text-leaf-800 uppercase tracking-wide mb-2">
          <MapPin size={14} /> {t("profile_location")}
        </p>
        <p className="text-sm text-ink-900">{location}</p>
      </Card>

      <Card className="mb-4">
        <p className="flex items-center gap-2 text-xs font-bold text-leaf-800 uppercase tracking-wide mb-3">
          <Sprout size={14} /> {t("profile_crops")}
        </p>
        <div className="flex flex-wrap gap-2">
          {crops.map((c) => (
            <Badge key={c} tone="success">{c}</Badge>
          ))}
        </div>
      </Card>

      <Card className="bg-soil-100 border-none">
        <p className="flex items-center gap-2 text-xs font-bold text-ink-600 uppercase tracking-wide mb-2">
          <Info size={14} /> {t("profile_about")}
        </p>
        <p className="text-sm text-ink-600 leading-snug">{t("profile_aboutText")}</p>
      </Card>
    </PageContainer>
  );
}
