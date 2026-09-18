import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import { useAsync } from "../hooks/useAsync";
import { FollowUp } from "../types";
import { EmptyState, ErrorState, Loader } from "../components/States";
import { formatDate } from "../utils/format";

export default function FollowUpsPage() {
  const { data, loading, error } = useAsync<FollowUp[]>(async () => (await api.get("/follow-ups/")).data, []);
  const [view, setView] = useState<"list" | "calendar">("list");
  const [filter, setFilter] = useState("all");
  const now = new Date();
  const start = new Date(now);
  start.setHours(0, 0, 0, 0);
  const end = new Date(now);
  end.setHours(23, 59, 59, 999);

  const filtered = useMemo(() => {
    return (data || []).filter((item) => {
      const due = new Date(item.due_date);
      if (filter === "today") return due >= start && due <= end;
      if (filter === "overdue") return due < start && item.status === "PENDING";
      if (filter === "upcoming") return due > end;
      return true;
    });
  }, [data, filter]);

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-2xl font-bold">Relances</h2>
        <div className="flex gap-2">
          {["all", "today", "overdue", "upcoming"].map((item) => (
            <button key={item} onClick={() => setFilter(item)} className={`rounded-xl px-3 py-2 text-sm ${filter === item ? "bg-blue-600 text-white" : "bg-white border"}`}>
              {item}
            </button>
          ))}
          <button onClick={() => setView(view === "list" ? "calendar" : "list")} className="rounded-xl border bg-white px-3 py-2 text-sm">
            {view === "list" ? "Calendrier" : "Liste"}
          </button>
        </div>
      </div>
      {filtered.length === 0 && <EmptyState title="Aucune relance" hint="Programmez une relance depuis une fiche prospect." />}
      {view === "list" ? (
        <div className="card divide-y">
          {filtered.map((item) => {
            const overdue = new Date(item.due_date) < start && item.status === "PENDING";
            return (
              <div key={item.id} className={`flex items-center justify-between px-4 py-3 ${overdue ? "bg-rose-50" : ""}`}>
                <div>
                  <p className="font-medium">Prospect #{item.prospect_id}</p>
                  <p className="text-sm text-slate-500">{item.notes}</p>
                </div>
                <div className="text-right">
                  <p className={overdue ? "font-semibold text-rose-600" : ""}>{formatDate(item.due_date)}</p>
                  <Link className="text-sm text-blue-600" to={`/prospects/${item.prospect_id}`}>
                    Ouvrir
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="card grid gap-3 p-5 md:grid-cols-7">
          {Array.from({ length: 14 }).map((_, index) => {
            const day = new Date();
            day.setDate(day.getDate() + index - 3);
            const items = filtered.filter((item) => new Date(item.due_date).toDateString() === day.toDateString());
            return (
              <div key={index} className="rounded-xl bg-slate-50 p-3 text-sm">
                <p className="font-semibold">{day.toLocaleDateString("fr-FR", { weekday: "short", day: "numeric" })}</p>
                {items.map((item) => (
                  <p key={item.id} className="mt-2 rounded bg-white p-2">
                    #{item.prospect_id}
                  </p>
                ))}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
