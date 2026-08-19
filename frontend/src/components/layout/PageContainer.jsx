export default function PageContainer({ children, className = "" }) {
  return (
    <main className={`max-w-md mx-auto px-4 pt-4 pb-28 ${className}`}>
      {children}
    </main>
  );
}
