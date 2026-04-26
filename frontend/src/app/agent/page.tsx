import { DashboardCard } from '@/components/dashboard-card';

export default function AgentPage() {
  return (
    <main className="p-6 grid gap-4">
      <h1 className="text-2xl font-bold">Human Agent Dashboard</h1>
      <DashboardCard title="Live Transcript">Arabic transcript stream placeholder.</DashboardCard>
      <DashboardCard title="Current Order">Items, modifiers, and total preview.</DashboardCard>
      <DashboardCard title="AI Summary">Reason for handoff and risks.</DashboardCard>
    </main>
  );
}
