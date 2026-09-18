export function formatMoney(value?: number | null) {
  return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(value || 0);
}

export function formatDate(value?: string | null) {
  if (!value) return "—";
  return new Date(value).toLocaleString("fr-FR", { dateStyle: "medium", timeStyle: "short" });
}

export const STATUSES = ["NEW", "QUALIFIED", "CONTACTED", "FOLLOW_UP", "NEGOTIATION", "CONVERTED", "LOST", "LATER"];
export const PRIORITIES = ["LOW", "MEDIUM", "HIGH", "VERY_HIGH"];
