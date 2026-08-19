import { twMerge } from "tailwind-merge";

export default function Card({ children, className = "", padded = true }) {
  return (
    <div
      className={twMerge(
        "bg-white rounded-2xl border border-soil-200 shadow-[0_2px_10px_rgba(47,82,51,0.06)]",
        padded ? "p-4" : "",
        className
      )}
    >
      {children}
    </div>
  );
}
