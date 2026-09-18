import { useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import { useAsync } from "../hooks/useAsync";
import { Activity, AIAnalysis, Contact, Conversion, FollowUp, Prospect, Qualification } from "../types";
import { EmptyState, ErrorState, Loader } from "../components/States";
import { PriorityBadge, ScoreBadge, StatusBadge } from "../components/Badges";
import Modal from "../components/Modal";
import { formatDate, formatMoney, PRIORITIES, STATUSES } from "../utils/format";
import { useToast } from "../context/ToastContext";
import { useAuth } from "../context/AuthContext";

const icons: Record<string, string> = { PHONE: "📞", EMAIL: "📧", MEETING: "📅", LINKEDIN: "💼", NOTE: "📝", OTHER: "🔔" };

export default function ProspectDetailPage() {
  const { id } = useParams();
  const { notify } = useToast();
  const { user } = useAuth();
  const prospectId = Number(id);
  const prospect = useAsync<Prospect>(async () => (await api.get(`/prospects/${prospectId}`)).data, [prospectId]);
  const contacts = useAsync<Contact[]>(async () => (await api.get("/contacts/", { params: { prospect_id: prospectId } })).data, [prospectId]);
  const activities = useAsync<Activity[]>(async () => (await api.get("/activities/", { params: { prospect_id: prospectId } })).data, [prospectId]);
  const followUps = useAsync<FollowUp[]>(async () => (await api.get("/follow-ups/")).data.then((items: FollowUp[]) => items.filter((item) => item.prospect_id === prospectId)), [prospectId]);
  const conversions = useAsync<Conversion[]>(async () => (await api.get("/conversions/")).data.then((items: Conversion[]) => items.filter((item) => item.prospect_id === prospectId)), [prospectId]);
  const qualification = useAsync<Qualification>(async () => (await api.post(`/prospects/${prospectId}/qualify`)).data, [prospectId]);
  const [ai, setAi] = useState<AIAnalysis | null>(null);
  const [modal, setModal] = useState<string | null>(null);
  const [confirmConvert, setConfirmConvert] = useState(false);

  const reloadAll = () => {
    prospect.reload();
    contacts.reload();
    activities.reload();
    followUps.reload();
    conversions.reload();
    qualification.reload();
  };

  const analyze = async () => {
    const { data } = await api.post(`/ai/prospects/${prospectId}/analyze`);
    setAi(data);
    notify("Analyse IA enregistrée");
    reloadAll();
  };

  const addActivity = async (type: string, subject: string, description: string) => {
    await api.post("/activities/", { prospect_id: prospectId, type, subject, description, completed_at: new Date().toISOString() });
    notify("Activité ajoutée");
    setModal(null);
    reloadAll();
  };

  const changeStatus = async (status: string) => {
    await api.patch(`/prospects/${prospectId}/status`, { status });
    notify("Statut mis à jour");
    reloadAll();
  };

  const convert = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api.post("/conversions/", {
      prospect_id: prospectId,
      department: form.get("department"),
      value: Number(form.get("value")) || prospect.data?.estimated_value,
      notes: form.get("notes"),
    });
    notify("Prospect converti et transmis");
    setConfirmConvert(false);
    reloadAll();
  };

  if (prospect.loading) return <Loader />;
  if (prospect.error) return <ErrorState message={prospect.error} />;
  if (!prospect.data) return <EmptyState title="Introuvable" hint="Ce prospect n'existe pas." />;
  const item = prospect.data;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold">{item.company?.name}</h2>
          <p className="text-slate-500">
            {item.company?.industry} · {item.company?.city}, {item.company?.country}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <StatusBadge status={item.status} />
          <PriorityBadge priority={item.priority} />
          <ScoreBadge score={item.score} />
        </div>
      </div>
      <div className="flex flex-wrap gap-2">
        {["NOTE", "PHONE", "EMAIL"].map((type) => (
          <button key={type} onClick={() => setModal(type)} className="rounded-xl border bg-white px-3 py-2 text-sm">
            {type === "NOTE" ? "Ajouter une note" : type === "PHONE" ? "Enregistrer un appel" : "Ajouter un email"}
          </button>
        ))}
        <button onClick={() => setModal("FOLLOW")} className="rounded-xl border bg-white px-3 py-2 text-sm">
          Programmer une relance
        </button>
        <select className="rounded-xl border px-3 py-2 text-sm" value={item.status} onChange={(e) => changeStatus(e.target.value)}>
          {STATUSES.map((status) => (
            <option key={status}>{status}</option>
          ))}
        </select>
        <button onClick={() => changeStatus("LOST")} className="rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-700">
          Classer perdu
        </button>
        <button onClick={() => changeStatus("LATER")} className="rounded-xl bg-orange-50 px-3 py-2 text-sm text-orange-700">
          Plus tard
        </button>
        <button onClick={() => setConfirmConvert(true)} className="rounded-xl bg-emerald-600 px-3 py-2 text-sm text-white">
          Convertir
        </button>
        <button onClick={analyze} className="rounded-xl bg-blue-600 px-3 py-2 text-sm text-white">
          Analyser avec l'IA
        </button>
      </div>
      <div className="grid gap-4 xl:grid-cols-3">
        <div className="card space-y-2 p-5 xl:col-span-2">
          <h3 className="font-semibold">Informations entreprise</h3>
          <p>Site : {item.company?.website || "—"}</p>
          <p>Email : {item.company?.email || "—"} · Tél. {item.company?.phone || "—"}</p>
          <p>Taille : {item.company?.employee_count || "—"} collaborateurs</p>
          <p className="text-slate-600">{item.company?.description}</p>
        </div>
        <div className="card p-5">
          <h3 className="font-semibold">Qualification</h3>
          <p className="mt-2 text-sm text-slate-500">Pourquoi ce score ?</p>
          <ul className="mt-3 space-y-2 text-sm">
            {qualification.data?.criteria.map((criterion) => (
              <li key={criterion.label} className="rounded-lg bg-slate-50 p-2">
                <span className="font-medium">{criterion.label}</span> (+{criterion.points}) — {criterion.explanation}
              </li>
            ))}
          </ul>
          <p className="mt-3 text-sm">{qualification.data?.summary}</p>
        </div>
      </div>
      {ai && (
        <div className="card p-5">
          <h3 className="font-semibold">Recommandation IA ({ai.provider})</h3>
          <p className="mt-2">{ai.recommendation}</p>
          <p className="mt-2 text-sm text-slate-600">Prochaine action : {ai.next_action}</p>
          <p className="mt-2 text-sm">Besoins : {ai.potential_needs.join(" · ")}</p>
          <pre className="mt-3 whitespace-pre-wrap rounded-xl bg-slate-50 p-3 text-sm">{ai.outreach_message}</pre>
        </div>
      )}
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="card p-5">
          <h3 className="font-semibold">Contacts</h3>
          <ul className="mt-3 space-y-2 text-sm">
            {contacts.data?.map((contact) => (
              <li key={contact.id}>
                {contact.first_name} {contact.last_name} — {contact.job_title} · {contact.email}
              </li>
            ))}
          </ul>
        </div>
        <div className="card p-5">
          <h3 className="font-semibold">Relances</h3>
          <ul className="mt-3 space-y-2 text-sm">
            {followUps.data?.map((itemFollow) => (
              <li key={itemFollow.id} className={new Date(itemFollow.due_date) < new Date() ? "text-rose-600" : ""}>
                {formatDate(itemFollow.due_date)} · {itemFollow.status} · {itemFollow.notes}
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="card p-5">
        <h3 className="font-semibold">Historique</h3>
        <ol className="mt-4 space-y-4">
          {activities.data?.map((activity) => (
            <li key={activity.id} className="border-l-2 border-blue-200 pl-4">
              <p className="text-xs text-slate-500">{formatDate(activity.created_at)}</p>
              <p className="font-medium">
                {icons[activity.type] || "🔔"} {activity.subject}
              </p>
              <p className="text-sm text-slate-600">{activity.description}</p>
            </li>
          ))}
        </ol>
      </div>
      {conversions.data && conversions.data.length > 0 && (
        <div className="card p-5">
          <h3 className="font-semibold">Historique de conversion</h3>
          {conversions.data.map((itemConversion) => (
            <p key={itemConversion.id} className="mt-2 text-sm">
              {formatDate(itemConversion.converted_at)} → {itemConversion.department} · {formatMoney(itemConversion.value)}
            </p>
          ))}
        </div>
      )}
      <Modal open={!!modal && modal !== "FOLLOW"} title="Nouvelle activité" onClose={() => setModal(null)}>
        <form
          className="space-y-3"
          onSubmit={(event) => {
            event.preventDefault();
            const form = new FormData(event.currentTarget);
            addActivity(modal || "NOTE", String(form.get("subject")), String(form.get("description")));
          }}
        >
          <input name="subject" className="w-full rounded-xl border px-3 py-2" placeholder="Sujet" required />
          <textarea name="description" className="w-full rounded-xl border px-3 py-2" placeholder="Détail" />
          <button className="w-full rounded-xl bg-blue-600 py-2 text-white">Enregistrer</button>
        </form>
      </Modal>
      <Modal open={modal === "FOLLOW"} title="Programmer une relance" onClose={() => setModal(null)}>
        <form
          className="space-y-3"
          onSubmit={async (event) => {
            event.preventDefault();
            const form = new FormData(event.currentTarget);
            await api.post("/follow-ups/", {
              prospect_id: prospectId,
              assigned_to: user?.id,
              due_date: form.get("due_date"),
              notes: form.get("notes"),
            });
            notify("Relance programmée");
            setModal(null);
            reloadAll();
          }}
        >
          <input name="due_date" type="datetime-local" className="w-full rounded-xl border px-3 py-2" required />
          <textarea name="notes" className="w-full rounded-xl border px-3 py-2" placeholder="Commentaire" />
          <button className="w-full rounded-xl bg-blue-600 py-2 text-white">Programmer</button>
        </form>
      </Modal>
      <Modal open={confirmConvert} title="Confirmer la conversion" onClose={() => setConfirmConvert(false)}>
        <form className="space-y-3" onSubmit={convert}>
          <p className="text-sm text-slate-600">Le prospect sera transmis au département choisi.</p>
          <select name="department" className="w-full rounded-xl border px-3 py-2">
            {["Commercial", "Support", "Technique", "Comptabilité", "Direction"].map((itemDept) => (
              <option key={itemDept}>{itemDept}</option>
            ))}
          </select>
          <input name="value" type="number" defaultValue={item.estimated_value || 0} className="w-full rounded-xl border px-3 py-2" />
          <textarea name="notes" className="w-full rounded-xl border px-3 py-2" placeholder="Notes de transmission" />
          <button className="w-full rounded-xl bg-emerald-600 py-2 text-white">Confirmer la conversion</button>
        </form>
      </Modal>
    </div>
  );
}
