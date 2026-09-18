export function Loader() {
  return <div className="animate-pulse rounded-xl bg-slate-100 p-8 text-center text-slate-500">Chargement…</div>;
}

export function EmptyState({ title, hint }: { title: string; hint: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-slate-300 p-10 text-center">
      <p className="font-semibold text-slate-700">{title}</p>
      <p className="mt-1 text-sm text-slate-500">{hint}</p>
    </div>
  );
}

export function ErrorState({ message }: { message: string }) {
  return <div className="rounded-xl bg-rose-50 p-4 text-sm text-rose-700">{message}</div>;
}
