export function StatusBadge({ status }: { status: string }) {
  const map: Record<string, string> = {
    NEW: "bg-slate-800/60 text-slate-300",
    QUALIFIED: "bg-sky-600/30 text-sky-300",
    CONTACTED: "bg-slate-800/60 text-slate-300",
    FOLLOW_UP: "bg-slate-800/60 text-slate-300",
    NEGOTIATION: "bg-slate-800/60 text-slate-300",
    CONVERTED: "bg-slate-800/60 text-slate-300",
    LOST: "bg-slate-800/60 text-slate-300",
    LATER: "bg-slate-800/60 text-slate-300",
  };
  return <span className={`rounded-full px-2.5 py-1 text-xs font-semibold bg-slate-900/80 border border-slate-700/30 ${map[status] || "bg-slate-900/80"}`}>{status}</span>;
}

export function PriorityBadge({ priority }: { priority: string }) {
  const map: Record<string, string> = {
    LOW: "bg-slate-800/60 text-slate-300",
    MEDIUM: "bg-sky-600/30 text-sky-300",
    HIGH: "bg-amber-600/30 text-sky-300",
    VERY_HIGH: "bg-rose-600/30 text-sky-300",
  };
  return <span className={`rounded-full px-2.5 py-1 text-xs font-semibold bg-slate-900/80 border border-slate-700/30 ${map[priority] || "bg-slate-900/80"}`}>{priority}</span>;
}

export function ScoreBadge({ score }: { score: number }) {
  const tone = score >= 81 ? "bg-sky-600/40 text-sky-300" : score >= 61 ? "bg-sky-500/40 text-sky-300" : score >= 31 ? "bg-amber-600/40 text-slate-300" : "bg-slate-900/80";
  return <span className={`rounded-full px-2.5 py-1 text-xs font-semibold bg-slate-900/80 border border-slate-700/30 ${tone}`}>{Math.round(score)}</span>;
}
