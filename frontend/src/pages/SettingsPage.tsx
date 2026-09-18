export default function SettingsPage() {
  const aiActions = [
    "Identifier des prospects",
    "Qualifier un prospect",
    "Calculer le score",
    "Expliquer le score",
    "Prioriser",
    "Détecter les besoins",
    "Recommander une action",
    "Générer un message",
    "Suggérer une relance",
    "Analyser la prospection",
    "Mettre à jour la priorité",
    "Estimer le potentiel",
    "Résumer l’historique",
  ];

  const sections = [
    {
      title: "Mon profil",
      fields: [
        { label: "Prénom", value: "Sofia" },
        { label: "Nom", value: "Martin" },
        { label: "Email", value: "sofia@prospectai.fr" },
        { label: "Langue", value: "Français" },
      ],
    },
    {
      title: "Entreprise",
      fields: [
        { label: "Nom de l’entreprise", value: "ProspectAI SAS" },
        { label: "Secteur", value: "B2B SaaS" },
        { label: "Pays", value: "France" },
        { label: "Devise", value: "EUR" },
      ],
    },
    {
      title: "IA",
      fields: [
        { label: "Fournisseur", value: "Google Gemini" },
        { label: "Modèle", value: "gemini-3.6-flash" },
        { label: "Température", value: "0.4" },
        { label: "Analyse automatique", value: "Activée" },
      ],
      extra: (
        <div className="mt-5 rounded-2xl border border-sky-500/20 bg-sky-500/10 p-4">
          <div className="mb-3 flex items-center justify-between">
            <h4 className="text-lg font-bold text-white">Parcours IA ProspectAI</h4>
            <span className="rounded-full border border-sky-400/40 bg-sky-400/10 px-2 py-1 text-[10px] uppercase tracking-[0.2em] text-sky-200">
              Identifier → Qualifier → Prospecter → Relancer → Convertir
            </span>
          </div>

          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {aiActions.map((action) => (
              <div key={action} className="rounded-xl border border-slate-700 bg-slate-950/40 px-3 py-2 text-sm text-slate-200">
                {action}
              </div>
            ))}
          </div>
        </div>
      ),
    },
    {
      title: "Qualification",
      fields: [
        { label: "Score minimum", value: "72" },
        { label: "Mots-clés priorisés", value: "lead, budget, décideur" },
        { label: "Seuil de relance", value: "48h" },
        { label: "Priorité d’audience", value: "PME / ETI" },
      ],
    },
    {
      title: "Notifications",
      fields: [
        { label: "Email de notification", value: "Activé" },
        { label: "Relances automatiques", value: "Oui" },
        { label: "Récapitulatif quotidien", value: "Envoyé" },
        { label: "Alertes critiques", value: "Urgentes" },
      ],
    },
    {
      title: "Utilisateurs",
      fields: [
        { label: "Rôle par défaut", value: "Manager" },
        { label: "2FA obligatoire", value: "Oui" },
        { label: "Invitation requise", value: "Activée" },
        { label: "Permissions par équipe", value: "Personnalisées" },
      ],
    },
    {
      title: "Sécurité",
      fields: [
        { label: "Session expirante", value: "30 min" },
        { label: "Vérification d’identité", value: "Requise" },
        { label: "Historique des connexions", value: "Actif" },
        { label: "Restrictions IP", value: "Par défaut" },
      ],
    },
    {
      title: "Données",
      fields: [
        { label: "Sauvegarde automatique", value: "Tous les jours" },
        { label: "Export CSV", value: "Disponible" },
        { label: "Retention", value: "12 mois" },
        { label: "Conformité RGPD", value: "Validée" },
      ],
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.28em] text-sky-300/80">Paramètres</p>
          <h2 className="mt-2 text-3xl font-black tracking-[-0.06em] text-white">Configuration</h2>
        </div>
        <button className="rounded-xl bg-gradient-to-r from-sky-400 to-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-sky-500/25 transition hover:opacity-95">
          Enregistrer
        </button>
      </div>

      <div className="grid gap-6 xl:grid-cols-[260px_minmax(0,1fr)]">
        <aside className="card p-3">
          <div className="space-y-1">
            {sections.map((section, index) => (
              <button
                key={section.title}
                type="button"
                className={`flex w-full items-center justify-between rounded-xl px-3 py-2.5 text-left text-sm transition ${
                  index === 0
                    ? "bg-sky-500/15 text-sky-200 ring-1 ring-sky-400/30"
                    : "text-slate-300 hover:bg-slate-800/80 hover:text-white"
                }`}
              >
                <span>{section.title}</span>
                <span className="text-[10px] uppercase tracking-[0.2em] text-slate-400">{index + 1}</span>
              </button>
            ))}
          </div>
        </aside>

        <div className="space-y-6">
          {sections.map((section) => (
            <section key={section.title} className="card p-6">
              <h3 className="text-2xl font-black tracking-[-0.04em] text-white">{section.title}</h3>

              <div className="mt-5 grid gap-4 md:grid-cols-2">
                {section.fields.map((field) => (
                  <div key={field.label}>
                    <label className="mb-2 block text-sm text-slate-300">{field.label}</label>
                    <div className="rounded-xl border border-slate-700 bg-slate-950/40 px-3 py-2.5 text-sm text-slate-100">
                      {field.value}
                    </div>
                  </div>
                ))}
              </div>

              {section.extra}
            </section>
          ))}
        </div>
      </div>
    </div>
  );
}
