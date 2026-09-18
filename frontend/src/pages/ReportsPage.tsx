import { useState } from "react";
import api from "../services/api";
import { useAsync } from "../hooks/useAsync";
import { Loader, ErrorState } from "../components/States";
import { formatMoney } from "../utils/format";

export default function ReportsPage() {
  const [industry, setIndustry] = useState("");
  const [status, setStatus] = useState("");
  const { data, loading, error, reload } = useAsync(async () => (await api.get("/reports/summary", { params: { industry: industry || undefined, status: status || undefined } })).data, [industry, status]);

  const exportCsv = async () => {
    const response = await api.get("/reports/export.csv", { responseType: "blob", params: { industry: industry || undefined, status: status || undefined } });
    const url = URL.createObjectURL(response.data);
    const link = document.createElement("a");
    link.href = url;
    link.download = "rapport-prospection.csv";
    link.click();
  };

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-2xl font-bold">Rapports</h2>
        <button onClick={exportCsv} className="rounded-xl bg-slate-900 px-4 py-2 text-sm text-white">
          Export CSV
        </button>
      </div>
      <div className="flex gap-3">
        <input value={industry} onChange={(e) => setIndustry(e.target.value)} placeholder="Secteur" className="rounded-xl border px-3 py-2" />
        <input value={status} onChange={(e) => setStatus(e.target.value)} placeholder="Statut" className="rounded-xl border px-3 py-2" />
        <button onClick={reload} className="rounded-xl border px-3 py-2">
          Filtrer
        </button>
      </div>
      <div className="grid gap-4 md:grid-cols-4">
        {[
          ["Générés", data.generated],
          ["Qualifiés", data.qualified],
          ["Contactés", data.contacted],
          ["Convertis", data.converted],
          ["Perdus", data.lost],
          ["Taux", `${data.conversion_rate}%`],
          ["Potentiel", formatMoney(data.potential_value)],
          ["Converti", formatMoney(data.converted_value)],
        ].map(([label, value]) => (
          <div key={String(label)} className="card p-5">
            <p className="text-sm text-slate-500">{label}</p>
            <p className="mt-2 text-2xl font-bold">{value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
