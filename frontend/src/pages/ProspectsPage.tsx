import { useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import api from "../services/api";
import { useAsync } from "../hooks/useAsync";
import { Company, Prospect, User } from "../types";
import { EmptyState, ErrorState, Loader } from "../components/States";
import { PriorityBadge, ScoreBadge, StatusBadge } from "../components/Badges";
import Modal from "../components/Modal";
import { formatMoney } from "../utils/format";
import { useToast } from "../context/ToastContext";

export default function ProspectsPage() {
  const { notify } = useToast();
  const [params, setParams] = useSearchParams();
  const [open, setOpen] = useState(false);
  const query = useMemo(() => Object.fromEntries(params.entries()), [params]);
  const { data, loading, error, reload } = useAsync(async () => {
    const response = await api.get("/prospects/", { params: { ...query, page: query.page || 1, page_size: 10 } });
    return response.data as { items: Prospect[]; total: number; page: number; page_size: number };
  }, [params.toString()]);
  const companies = useAsync<Company[]>(async () => (await api.get("/companies/")).data, []);
  const users = useAsync<User[]>(async () => (await api.get("/users/directory")).data, []);

  const setFilter = (key: string, value: string) => {
    const next = new URLSearchParams(params);
    if (value) next.set(key, value);
    else next.delete(key);
    next.set("page", "1");
    setParams(next);
  };

  const createProspect = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api.post("/prospects/", {
      company_id: Number(form.get("company_id")),
      assigned_to: Number(form.get("assigned_to")) || null,
      notes: form.get("notes"),
      estimated_value: Number(form.get("estimated_value")) || 0,
    });
    notify("Prospect créé");
    setOpen(false);
    reload();
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold">Prospects</h2>
          <p className="text-slate-500">Filtrez, qualifiez et priorisez le portefeuille.</p>
        </div>
        <div className="hidden lg:flex items-center gap-2">
          <button onClick={() => setOpen(true)} className="rounded-xl bg-sky-500/20 px-3 py-1 text-sm font-medium text-sky-300 border border-sky-500/30 hover:bg-sky-500/30 transition-colors">
            Nouveau prospect
          </button>
        </div>
      </div>
      <div className="card p-4 md:grid-cols-4 lg:grid-cols-7">
        <input defaultValue={query.search || ""} placeholder="Recherche" className="rounded-xl border border-slate-400 bg-slate-900/50 px-3 py-2 text-sm w-full" onBlur={(e) => setFilter("search", e.target.value)} />
        <select className="rounded-xl border border-slate-400 bg-slate-900/50 px-3 py-2 text-sm w-full" value={query.status || ""} onChange={(e) => setFilter("status", e.target.value)}>
          <option value="">Statut</option>
          {["NEW", "QUALIFIED", "CONTACTED", "FOLLOW_UP", "NEGOTIATION", "CONVERTED", "LOST", "LATER"].map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>
        <select className="rounded-xl border border-slate-400 bg-slate-900/50 px-3 py-2 text-sm w-full" value={query.priority || ""} onChange={(e) => setFilter("priority", e.target.value)}>
          <option value="">Priorité</option>
          {["LOW", "MEDIUM", "HIGH", "VERY_HIGH"].map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>
        <input placeholder="Secteur" className="rounded-xl border border-slate-400 bg-slate-900/50 px-3 py-2 text-sm w-full" defaultValue={query.industry || ""} onBlur={(e) => setFilter("industry", e.target.value)} />
        <input placeholder="Ville" className="rounded-xl border border-slate-400 bg-slate-900/50 px-3 py-2 text-sm w-full" defaultValue={query.city || ""} onBlur={(e) => setFilter("city", e.target.value)} />
        <input type="number" placeholder="Score min" className="rounded-xl border border-slate-400 bg-slate-900/50 px-3 py-2 text-sm w-full" defaultValue={query.min_score || ""} onBlur={(e) => setFilter("min_score", e.target.value)} />
        <select className="rounded-xl border border-slate-400 bg-slate-900/50 px-3 py-2 text-sm w-full" value={query.sort || "created_at"} onChange={(e) => setFilter("sort", e.target.value)}>
          <option value="created_at">Date</option>
          <option value="score">Score</option>
          <option value="estimated_value">Valeur</option>
        </select>
      </div>
      {loading && <Loader />}
      {error && <ErrorState message={error} />}
      {data && data.items.length === 0 && <EmptyState title="Aucun prospect" hint="Créez un prospect ou importez depuis la prospection." />}
      {data && data.items.length > 0 && (
        <div className="card overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-4 py-3">Entreprise</th>
                <th>Statut</th>
                <th>Priorité</th>
                <th>Score</th>
                <th>Valeur</th>
                <th>Commercial</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((item) => (
                <tr key={item.id} className="border-t">
                  <td className="px-4 py-3">
                    <Link to={`/prospects/${item.id}`} className="font-medium text-blue-700">
                      {item.company?.name}
                    </Link>
                    <p className="text-xs text-slate-500">
                      {item.company?.city} · {item.company?.industry}
                    </p>
                  </td>
                  <td>
                    <StatusBadge status={item.status} />
                  </td>
                  <td>
                    <PriorityBadge priority={item.priority} />
                  </td>
                  <td>
                    <ScoreBadge score={item.score} />
                  </td>
                  <td>{formatMoney(item.estimated_value)}</td>
                  <td>{item.assigned_user?.name || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="flex justify-end gap-2 p-3">
            <button
              className="rounded-lg border px-3 py-1 text-sm"
              disabled={data.page <= 1}
              onClick={() => setFilter("page", String(data.page - 1))}
            >
              Précédent
            </button>
            <button
              className="rounded-lg border px-3 py-1 text-sm"
              disabled={data.page * data.page_size >= data.total}
              onClick={() => setFilter("page", String(data.page + 1))}
            >
              Suivant
            </button>
          </div>
        </div>
      )}
      <Modal open={open} title="Nouveau prospect" onClose={() => setOpen(false)}>
        <form className="space-y-3" onSubmit={createProspect}>
          <select name="company_id" className="w-full rounded-xl border px-3 py-2" required>
            {companies.data?.map((company) => (
              <option key={company.id} value={company.id}>
                {company.name}
              </option>
            ))}
          </select>
          <select name="assigned_to" className="w-full rounded-xl border px-3 py-2">
            {users.data?.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>
          <input name="estimated_value" type="number" placeholder="Valeur estimée" className="w-full rounded-xl border px-3 py-2" />
          <textarea name="notes" placeholder="Notes" className="w-full rounded-xl border px-3 py-2" />
          <button className="w-full rounded-xl bg-blue-600 py-2 text-white">Créer</button>
        </form>
      </Modal>
    </div>
  );
}
