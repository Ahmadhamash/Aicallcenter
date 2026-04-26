import { DashboardCard } from '@/components/dashboard-card';

export default function AdminPage() {
  return (
    <main className="p-6 grid gap-4">
      <h1 className="text-2xl font-bold">SaaS Admin Dashboard</h1>
      <DashboardCard title="Restaurants & Subscriptions">Tenant lifecycle and billing status.</DashboardCard>
      <DashboardCard title="Users & Roles">Platform admins, owners, and agents.</DashboardCard>
      <DashboardCard title="Call Logs & AI Costs">Global usage and spend insights.</DashboardCard>
      <DashboardCard title="System Health">Realtime bridge status and queue metrics.</DashboardCard>
    </main>
  );
}
