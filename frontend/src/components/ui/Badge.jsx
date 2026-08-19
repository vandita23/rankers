const styles = {
  warning: "bg-marigold-100 text-clay-500",
  info: "bg-leaf-100 text-leaf-800",
  success: "bg-leaf-100 text-leaf-700",
  neutral: "bg-soil-100 text-ink-600",
};

export default function Badge({ children, tone = "neutral", className = "" }) {
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-semibold ${styles[tone]} ${className}`}
    >
      {children}
    </span>
  );
}
