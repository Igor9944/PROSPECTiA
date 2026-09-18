import { FormEvent, useState } from "react";
import api from "../services/api";
import { useToast } from "../context/ToastContext";
import { ScoreBadge } from "../components/Badges";
import { EmptyState } from "../components/States";

interface Result {
  name: string;
  industry: string;
  city: string;
  country: string;
  employee_count: number;
  website: string;
  description: string;
  potential_score: number;
  company_type: string;
}

export default function ProspectingPage() {
  const { notify } = useToast();
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);

  const search = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    setLoading(true);
    try {
      const { data } = await api.post("/prospecting/search", {
        industry: form.get("industry") || null,
        city: form.get("city") || null,
        country: form.get("country") || null,
        min_employees: form.get("min_employees") ? Number(form.get("min_employees")) : null,
        max_employees: form.get("max_employees") ? Number(form.get("max_employees")) : null,
        company_type: form.get("company_type") || null,
        keywords: form.get("keywords") || null,
        needs: form.get("needs") || null,
      });
      setResults(data);
    } finally {
      setLoading(false);
    }
  };

  const add = async (result: Result) => {
    await api.post("/prospecting/import", {
      name: result.name,
      industry: result.industry,
      city: result.city,
      country: result.country,
      employee_count: result.employee_count,
      website: result.website,
      description: result.description,
      source: "prospection-demo",
    });
    notify(`${result.name} ajouté aux prospects`);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Identification</h2>
        <p className="text-slate-500">Recherchez des entreprises fictives de démonstration, puis ajoutez-les au pipeline.</p>
      </div>
      <form onSubmit={search} className="card grid gap-3 p-5 md:grid-cols-4">
        <input name="industry" placeholder="Domaine d'activité" className="rounded-xl border px-3 py-2" />
        <input name="city" placeholder="Localisation" className="rounded-xl border px-3 py-2" />
        <input name="min_employees" type="number" placeholder="Taille min" className="rounded-xl border px-3 py-2" />
        <input name="max_employees" type="number" placeholder="Taille max" className="rounded-xl border px-3 py-2" />
        <input name="company_type" placeholder="Type d'entreprise" className="rounded-xl border px-3 py-2" />
        <input name="keywords" placeholder="Mots-clés" className="rounded-xl border px-3 py-2" />
        <input name="needs" placeholder="Besoins recherchés" className="rounded-xl border px-3 py-2" />
        <button className="rounded-xl bg-blue-600 text-white">{loading ? "Recherche…" : "Rechercher"}</button>
      </form>
      {results.length === 0 && <EmptyState title="Aucun résultat" hint="Lancez une recherche. Les données sont des mocks de démonstration." />}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {results.map((result) => (
          <article key={result.name} className="card p-5">
            <div className="flex items-start justify-between">
              <h3 className="font-semibold">{result.name}</h3>
              <ScoreBadge score={result.potential_score} />
            </div>
            <p className="mt-1 text-sm text-slate-500">
              {result.industry} · {result.city}, {result.country} · {result.employee_count} pers.
            </p>
            <a className="text-sm text-blue-600" href={result.website} target="_blank" rel="noreferrer">
              {result.website}
            </a>
            <p className="mt-3 text-sm text-slate-600">{result.description}</p>
            <button onClick={() => add(result)} className="mt-4 w-full rounded-xl bg-slate-900 py-2 text-sm text-white">
              Ajouter aux prospects
            </button>
          </article>
        ))}
      </div>
    </div>
  );
}
