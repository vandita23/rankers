import { twMerge } from "tailwind-merge";

const variants = {
  primary:
    "bg-leaf-800 text-white hover:bg-leaf-700 active:bg-leaf-900 disabled:bg-leaf-400",
  secondary:
    "bg-leaf-100 text-leaf-800 hover:bg-leaf-100/70 active:bg-leaf-100/90",
  outline:
    "bg-white text-leaf-800 border-2 border-leaf-800 hover:bg-leaf-100",
  marigold:
    "bg-marigold-500 text-leaf-900 hover:brightness-95 active:brightness-90",
  ghost: "bg-transparent text-ink-600 hover:bg-soil-100",
};

export default function Button({
  children,
  variant = "primary",
  className = "",
  icon: Icon,
  ...props
}) {
  return (
    <button
      className={twMerge(
        "inline-flex items-center justify-center gap-2 min-h-[52px] px-5 rounded-xl font-semibold text-[15px] transition-colors disabled:cursor-not-allowed disabled:opacity-60",
        variants[variant],
        className
      )}
      {...props}
    >
      {Icon && <Icon size={20} strokeWidth={2.25} />}
      {children}
    </button>
  );
}
