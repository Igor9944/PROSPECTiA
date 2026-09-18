import { Link } from "react-router-dom";
import api from "../services/api";
import { useAsync } from "../hooks/useAsync";
import { Activity } from "../types";
import { EmptyState, ErrorState, Loader } from "../components/States";
import { formatDate } from "../utils/format";

export default function ActivitiesPage() {
  const { data, loading, error } = useAsync<Activity[]>(async () => (await api.get("/activities/")).data, []);
  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;
  if (!data?.length) return <EmptyState title="Aucune activité" hint="Les actions commerciales apparaîtront ici." />;
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Activités</h2>
      <div className="card divide-y">
        {data.map((item) => (
          <div key={item.id} className="px-4 py-3">
            <p className="text-xs text-slate-500">{formatDate(item.created_at)}</p>
            <p className="font-medium">
              {item.type} · {item.subject}
            </p>
            <Link className="text-sm text-blue-600" to={`/prospects/${item.prospect_id}`}>
              Voir le prospect
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
