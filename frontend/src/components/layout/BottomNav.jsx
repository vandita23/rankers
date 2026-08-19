import { NavLink } from "react-router-dom";
import { Home, MessageCircleQuestion, Leaf, CloudSun, Landmark } from "lucide-react";
import { useApp } from "../../context/AppContext";

export default function BottomNav() {
  const { t } = useApp();

  const items = [
    { to: "/", label: t("nav_home"), icon: Home, end: true },
    { to: "/ask", label: t("nav_ask"), icon: MessageCircleQuestion },
    { to: "/disease", label: t("nav_disease"), icon: Leaf },
    { to: "/weather", label: t("nav_weather"), icon: CloudSun },
    { to: "/schemes", label: t("nav_schemes"), icon: Landmark },
  ];

  return (
    <nav className="fixed bottom-0 inset-x-0 z-30 bg-white border-t border-soil-200 pb-[env(safe-area-inset-bottom)]">
      <div className="max-w-md mx-auto grid grid-cols-5">
        {items.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex flex-col items-center justify-center gap-1 py-2.5 min-h-[60px] text-[11px] font-semibold transition-colors ${
                isActive ? "text-leaf-800" : "text-ink-400"
              }`
            }
          >
            {({ isActive }) => (
              <>
                <span
                  className={`grid place-items-center w-9 h-9 rounded-full ${
                    isActive ? "bg-leaf-100" : ""
                  }`}
                >
                  <Icon size={20} strokeWidth={2.25} />
                </span>
                <span className="leading-none text-center px-0.5">{label}</span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
