import { useEffect, useState } from "react";
import { CloudSun, CloudRain, Cloud, Sun, Droplets, Wind, Sparkles, Loader2 } from "lucide-react";
import { useApp } from "../context/AppContext";
import PageContainer from "../components/layout/PageContainer";
import Card from "../components/ui/Card";
import SectionHeading from "../components/ui/SectionHeading";
import { getWeather } from "../lib/api";

const conditionIcon = { rain: CloudRain, cloud: Cloud, sun: Sun };
const FALLBACK_LOCATION = "Barabanki, Uttar Pradesh";

export default function Weather() {
  const { t, lang, dashboard } = useApp();
  const location = dashboard?.farmer?.location || FALLBACK_LOCATION;
  const crop = dashboard?.farmer?.crops?.[0];

  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    getWeather(location, crop, lang)
      .then((data) => {
        if (!cancelled) setWeather(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message ?? "Failed to load weather");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [location, crop, lang]);

  return (
    <PageContainer>
      <div className="mb-4">
        <h1 className="font-display text-xl font-extrabold text-leaf-900">{t("weather_title")}</h1>
        <p className="text-ink-600 text-sm mt-1">{t("weather_subtitle")}</p>
      </div>

      {loading && (
        <Card className="mb-4 flex items-center justify-center py-10 text-ink-400">
          <Loader2 size={22} className="animate-spin" />
        </Card>
      )}

      {!loading && error && (
        <Card className="mb-4 border-clay-500/40 bg-marigold-100 text-sm text-ink-900">{error}</Card>
      )}

      {!loading && weather && (
        <>
          {/* Current conditions */}
          <Card className="mb-4 bg-leaf-800 text-white border-none">
            <p className="text-leaf-100/90 text-sm font-medium">{weather.location}</p>
            <div className="flex items-center justify-between mt-2">
              <div>
                <p className="font-display text-4xl font-extrabold leading-none">{weather.today.tempC}°</p>
                <p className="text-leaf-100/90 text-sm mt-1.5">{weather.today.condition}</p>
              </div>
              <CloudSun size={56} strokeWidth={1.5} className="text-marigold-500" />
            </div>
            <div className="grid grid-cols-3 gap-2 mt-4 pt-4 border-t border-white/15">
              <div className="flex flex-col items-center gap-1">
                <Droplets size={16} className="text-leaf-100/90" />
                <p className="text-xs text-leaf-100/90">{t("weather_humidity")}</p>
                <p className="text-sm font-bold">{weather.today.humidity}%</p>
              </div>
              <div className="flex flex-col items-center gap-1">
                <Wind size={16} className="text-leaf-100/90" />
                <p className="text-xs text-leaf-100/90">{t("weather_wind")}</p>
                <p className="text-sm font-bold">{weather.today.windKmh} km/h</p>
              </div>
              <div className="flex flex-col items-center gap-1">
                <CloudRain size={16} className="text-leaf-100/90" />
                <p className="text-xs text-leaf-100/90">{t("weather_rain")}</p>
                <p className="text-sm font-bold">{weather.today.rainChance}%</p>
              </div>
            </div>
          </Card>

          {/* AI recommendation */}
          <Card className="mb-4 bg-marigold-100 border-marigold-500/30">
            <p className="flex items-center gap-1.5 font-display font-bold text-leaf-900 text-sm mb-2">
              <Sparkles size={16} className="text-clay-500" /> {t("weather_recommendation")}
            </p>
            <p className="text-sm text-ink-900 leading-snug">{weather.recommendation}</p>
          </Card>

          {/* Forecast */}
          <section>
            <SectionHeading title={t("weather_forecast")} />
            <Card padded={false}>
              <div className="grid grid-cols-5 divide-x divide-soil-200">
                {weather.forecast.map((d, i) => {
                  const Icon = conditionIcon[d.condition] ?? Sun;
                  return (
                    <div key={i} className="flex flex-col items-center gap-1.5 py-4 px-1">
                      <p className="text-xs font-semibold text-ink-600">{d.day}</p>
                      <Icon
                        size={20}
                        className={
                          d.condition === "rain"
                            ? "text-leaf-700"
                            : d.condition === "sun"
                            ? "text-marigold-500"
                            : "text-ink-400"
                        }
                      />
                      <p className="text-sm font-bold text-ink-900">{d.tempC}°</p>
                      <p className="text-[10px] text-ink-400">{d.rain}%</p>
                    </div>
                  );
                })}
              </div>
            </Card>
          </section>
        </>
      )}
    </PageContainer>
  );
}
