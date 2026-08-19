export default function SectionHeading({ title, action }) {
  return (
    <div className="flex items-center justify-between mb-3">
      <h2 className="font-display text-lg font-bold text-leaf-900">{title}</h2>
      {action}
    </div>
  );
}
