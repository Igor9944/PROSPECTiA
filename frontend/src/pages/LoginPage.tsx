import { FormEvent, useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import BrandMark from "../components/BrandMark";

export default function LoginPage() {
  const { user, login } = useAuth();
  const { notify } = useToast();
  const [email, setEmail] = useState("commercial@example.com");
  const [password, setPassword] = useState("Commercial123!");
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/" replace />;

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
    } catch {
      notify("Identifiants incorrects", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-shell flex min-h-screen items-center justify-center p-6 text-white">
      <div className="grid w-full max-w-6xl overflow-hidden rounded-[32px] border border-slate-700/70 bg-slate-900/40 shadow-[0_30px_80px_rgba(2,6,23,0.75)] backdrop-blur-xl lg:grid-cols-[1.1fr_0.9fr]">
        <div className="relative flex flex-col justify-between border-b border-slate-700/70 p-8 lg:border-b-0 lg:border-r">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(56,189,248,0.18),_transparent_30%),radial-gradient(circle_at_bottom_right,_rgba(59,130,246,0.2),_transparent_25%)]" />
          <div className="relative z-10">
            <div className="flex items-center gap-3">
              <BrandMark className="h-14 w-14" compact />
              <div>
                <div className="brand-word text-3xl font-black tracking-[-0.08em]">ProspectAI</div>
                <p className="text-[10px] uppercase tracking-[0.28em] text-sky-200/80">AI CRM</p>
              </div>
            </div>

            <div className="mt-12 max-w-md">
              <p className="text-sm uppercase tracking-[0.28em] text-sky-200/80">Leadership intelligente</p>
              <h1 className="mt-4 text-4xl font-black leading-tight tracking-[-0.05em] text-white">
                Mettez chaque opportunité sur la bonne voie.
              </h1>
              <p className="mt-4 text-base text-slate-300">
                Centralisez la prospection, qualifiez les prospects en temps réel et transformez chaque contact en pipeline rentable.
              </p>
            </div>
          </div>

          <div className="relative z-10 mt-12 grid gap-4 sm:grid-cols-3">
            {[
              ["+42%", "qualif. plus rapide"],
              ["12k", "contacts suivis"],
              ["24h", "retour sur relance"],
            ].map(([value, label]) => (
              <div key={label} className="rounded-2xl border border-slate-700/70 bg-slate-950/40 p-4 backdrop-blur-sm">
                <div className="text-2xl font-black text-white">{value}</div>
                <div className="mt-1 text-xs uppercase tracking-[0.2em] text-slate-400">{label}</div>
              </div>
            ))}
          </div>
        </div>

        <form onSubmit={onSubmit} className="glass-panel w-full p-8 text-white lg:p-9">
          <div className="text-center">
            <p className="text-xs uppercase tracking-[0.3em] text-sky-200/80">Connexion</p>
            <h2 className="mt-3 text-3xl font-black tracking-[-0.06em] text-white">Bienvenue</h2>
          </div>

          <div className="mt-8 space-y-4">
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-200">Email</label>
              <input className="soft-input" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-200">Mot de passe</label>
              <input type="password" className="soft-input" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
          </div>

          <button disabled={loading} className="primary-button mt-6">
            {loading ? "Connexion…" : "Se connecter"}
          </button>

          <p className="mt-5 text-center text-sm text-slate-300">
            Pas de compte ? <Link to="/register" className="font-semibold text-sky-300 hover:text-sky-200">Créer un compte</Link>
          </p>

          <div className="mt-4 text-center text-xs text-slate-400">
            <Link to="/conditions-utilisation" className="hover:text-sky-300">
              Conditions d’utilisation
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
