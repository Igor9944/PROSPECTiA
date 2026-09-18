import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Link } from "react-router-dom";
import api from "../services/api";
import { useAsync } from "../hooks/useAsync";
import { DashboardData } from "../types";
import { EmptyState, ErrorState, Loader } from "../components/States";
import { PriorityBadge, ScoreBadge, StatusBadge } from "../components/Badges";
import { formatMoney } from "../utils/format";

const COLORS = ["#2563eb", "#0ea5e9", "#8b5cf6", "#f59e0b", "#10b981", "#f43f5e", "#64748b", "#fb923c"];

export default function DashboardPage() {
  const { data, loading, error } = useAsync<DashboardData>(async () => (await api.get("/reports/dashboard")).data, []);
  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;
  if (!data) return <EmptyState title="Aucune donnée" hint="Lancez le script seed.py" />;

  const kpis = [
    { label: "Prospects", value: data.total },
    { label: "Nouveaux", value: data.new },
    { label: "Qualifiés", value: data.qualified },
    { label: "À relancer", value: data.to_follow },
    { label: "Convertis", value: data.converted },
    { label: "Perdus", value: data.lost },
    { label: "Valeur estimée", value: formatMoney(data.potential_value) },
    { label: "Taux conversion", value: `${data.conversion_rate}%` },
  ];

  const statusData = Object.entries(data.by_status || {}).map(([name, value]) => ({ name, value }));
  const priorityData = Object.entries(data.by_priority || {}).map(([name, value]) => ({ name, value }));
  const industryData = Object.entries(data.by_industry || {}).map(([name, value]) => ({ name, value }));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Tableau de bord</h2>
        <p className="text-slate-500">Vos priorités du jour et la prochaine action commerciale.</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {kpis.map((item) => (
          <div key={item.label} className="card p-5">
            <p className="text-sm text-slate-500">{item.label}</p>
            <p className="mt-2 text-2xl font-bold">{item.value}</p>
          </div>
        ))}
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <div className="card p-5">
          <h3 className="mb-4 font-semibold">Prospects par statut</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#2563eb" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card p-5">
          <h3 className="mb-4 font-semibold">Prospects par priorité</h3>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={priorityData} dataKey="value" nameKey="name" outerRadius={90}>
                {priorityData.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="card p-5">
          <h3 className="mb-4 font-semibold">Prospects par secteur</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={industryData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card p-5">
          <h3 className="mb-4 font-semibold">Évolution de la prospection</h3>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={data.evolution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="count" stroke="#8b5cf6" />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="card p-5 xl:col-span-2">
          <h3 className="mb-4 font-semibold">Conversion mensuelle</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={data.monthly_conversions}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="card p-5">
          <h3 className="mb-4 font-semibold">Relances du jour</h3>
          {data.today_follow_ups.length === 0 ? (
            <p className="text-sm text-slate-500">Aucune relance aujourd'hui.</p>
          ) : (
            <ul className="space-y-3">
              {data.today_follow_ups.map((item) => (
                <li key={item.id} className="flex items-center justify-between rounded-xl bg-amber-50 px-3 py-2">
                  <span>Prospect #{item.prospect_id}</span>
                  <Link className="text-sm text-blue-600" to={`/prospects/${item.prospect_id}`}>
                    Ouvrir
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="card p-5">
          <h3 className="mb-4 font-semibold">Prospects prioritaires</h3>
          <ul className="space-y-3">
            {data.priority_prospects.map((item) => (
              <li key={item.id} className="flex items-center justify-between gap-3">
                <Link to={`/prospects/${item.id}`} className="font-medium hover:text-blue-600">
                  {item.company?.name || `Prospect #${item.id}`}
                </Link>
                <div className="flex gap-2">
                  <ScoreBadge score={item.score} />
                  <PriorityBadge priority={item.priority} />
                  <StatusBadge status={item.status} />
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
