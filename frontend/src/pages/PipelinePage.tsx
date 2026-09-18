import api from "../services/api";
import { useAsync } from "../hooks/useAsync";
import { Prospect } from "../types";
import { Loader, ErrorState } from "../components/States";
import { ScoreBadge } from "../components/Badges";
import { Link } from "react-router-dom";
import { useToast } from "../context/ToastContext";
import { STATUSES } from "../utils/format";

export default function PipelinePage() {
  const { notify } = useToast();
  const { data, loading, error, reload } = useAsync<Prospect[]>(async () => (await api.get("/prospects/pipeline")).data, []);

  const move = async (id: number, status: string) => {
    await api.patch(`/prospects/${id}/status`, { status });
    notify("Pipeline mis à jour");
    reload();
  };

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Pipeline commercial</h2>
      <div className="flex gap-4 overflow-x-auto pb-4">
        {STATUSES.map((status) => (
          <section key={status} className="min-w-[240px] flex-1 rounded-2xl bg-slate-100 p-3">
            <h3 className="mb-3 text-sm font-semibold">{status}</h3>
            <div className="space-y-3">
              {data
                ?.filter((item) => item.status === status)
                .map((item) => (
                  <article key={item.id} className="rounded-xl bg-white p-3 shadow-sm">
                    <Link to={`/prospects/${item.id}`} className="font-medium">
                      {item.company?.name}
                    </Link>
                    <div className="mt-2">
                      <ScoreBadge score={item.score} />
                    </div>
                    <select className="mt-2 w-full rounded-lg border px-2 py-1 text-xs" value={item.status} onChange={(e) => move(item.id, e.target.value)}>
                      {STATUSES.map((option) => (
                        <option key={option}>{option}</option>
                      ))}
                    </select>
                  </article>
                ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
