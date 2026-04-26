export function DashboardCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="card">
      <h3 className="font-semibold mb-3">{title}</h3>
      {children}
    </section>
  );
}
