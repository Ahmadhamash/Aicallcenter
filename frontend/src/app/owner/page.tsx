import { DashboardCard } from '@/components/dashboard-card';

export default function OwnerPage() {
  return (
    <main className="p-6 grid gap-4">
      <h1 className="text-2xl font-bold">Restaurant Owner Dashboard</h1>
      <DashboardCard title="Menu Management">CRUD categories/items/modifiers and availability toggles.</DashboardCard>
      <DashboardCard title="Orders & Calls">Recent orders, recordings, transcripts.</DashboardCard>
      <DashboardCard title="Analytics">Conversion, AHT, escalation ratio, AI cost.</DashboardCard>
      <DashboardCard title="Branches & Hours">Branch-level configurations and schedules.</DashboardCard>
    </main>
  );
}
