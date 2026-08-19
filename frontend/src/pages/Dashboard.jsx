import { Link } from "react-router-dom";
import {
  MessageCircleQuestion,
  Leaf,
  CloudSun,
  Landmark,
  TriangleAlert,
  Info,
  CheckCircle2,
  Circle,
  ChevronRight,
} from "lucide-react";
import { useApp } from "../context/AppContext";
import PageContainer from "../components/layout/PageContainer";
import Card from "../components/ui/Card";
import Badge from "../components/ui/Badge";
import SectionHeading from "../components/ui/SectionHeading";
import { farmer, alerts, actionPlan } from "../data/mock";

function getGreetingKey() {
  const hour = new Date().getHours();
  if (hour < 12) return "greetingMorning";
  if (hour < 17) return "greetingAfternoon";
  return "greetingEvening";
}

export default function Dashboard() {
  const { t, lang } = useApp();
  const name = lang === "hi" ? farmer.nameHi : farmer.name;
  const location = lang === "hi" ? farmer.locationHi : farmer.location;

  const quickActions = [
    { to: "/ask", icon: MessageCircleQuestion, title: t("action_askAI"), desc: t("action_askAI_desc"), tone: "bg-leaf-800" },
    { to: "/disease", icon: Leaf, title: t("action_disease"), desc: t("action_disease_desc"), tone: "bg-leaf-600" },
    { to: "/weather", icon: CloudSun, title: t("action_weather"), desc: t("action_weather_desc"), tone: "bg-marigold-500" },
    { to: "/schemes", icon: Landmark, title: t("action_schemes"), desc: t("action_schemes_desc"), tone: "bg-clay-500" },
  ];

  return (
    <PageContainer>
      {/* Hero / greeting */}
      <section className="leaf-texture rounded-2xl bg-leaf-800 text-white px-5 py-6 mb-5 relative overflow-hidden">
        <p className="text-leaf-100/90 text-sm font-medium">{t(getGreetingKey())},</p>
        <h1 className="font-display text-2xl font-extrabold mt-0.5">{name} 👋</h1>
        <p className="text-leaf-100/90 text-sm mt-1">{location}</p>
      </section>

      {/* Quick actions */}
      <section className="mb-6">
        <SectionHeading title={t("home_quickActions")} />
        <div className="grid grid-cols-2 gap-3">
          {quickActions.map(({ to, icon: Icon, title, desc, tone }) => (
            <Link key={to} to={to}>
              <Card className="h-full active:scale-[0.98] transition-transform">
                <span className={`grid place-items-center w-11 h-11 rounded-xl ${tone} text-white mb-3`}>
                  <Icon size={22} strokeWidth={2.25} />
                </span>
                <p className="font-display font-bold text-leaf-900 text-[15px] leading-tight">{title}</p>
                <p className="text-ink-400 text-xs mt-1 leading-snug">{desc}</p>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* Alerts */}
      <section className="mb-6">
        <SectionHeading title={t("home_alerts")} />
        {alerts.length === 0 ? (
          <Card className="text-ink-600 text-sm">{t("home_noAlerts")}</Card>
        ) : (
          <div className="space-y-2.5">
            {alerts.map((a) => (
              <Card key={a.id} className="flex items-start gap-3">
                <span className={a.level === "warning" ? "text-clay-500" : "text-leaf-700"}>
                  {a.level === "warning" ? <TriangleAlert size={20} /> : <Info size={20} />}
                </span>
                <p className="text-sm text-ink-900 leading-snug">
                  {lang === "hi" ? a.text_hi : a.text_en}
                </p>
              </Card>
            ))}
          </div>
        )}
      </section>

      {/* Today's action plan */}
      <section>
        <SectionHeading title={t("home_todaysPlan")} />
        <Card padded={false}>
          <ul>
            {actionPlan.map((item, i) => (
              <li
                key={item.id}
                className={`flex items-center gap-3 px-4 py-3.5 ${
                  i !== actionPlan.length - 1 ? "border-b border-soil-200" : ""
                }`}
              >
                {item.done ? (
                  <CheckCircle2 size={20} className="text-leaf-600 shrink-0" />
                ) : (
                  <Circle size={20} className="text-ink-400 shrink-0" />
                )}
                <span
                  className={`text-sm leading-snug ${
                    item.done ? "text-ink-400 line-through" : "text-ink-900"
                  }`}
                >
                  {lang === "hi" ? item.text_hi : item.text_en}
                </span>
              </li>
            ))}
          </ul>
        </Card>
      </section>
    </PageContainer>
  );
}
