import { FormEvent, useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import BrandMark from "../components/BrandMark";

export default function RegisterPage() {
  const { user, register } = useAuth();
  const { notify } = useToast();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  if (user) return <Navigate to="/" replace />;

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    try {
      await register(name, email, password);
    } catch {
      notify("Inscription impossible", "error");
    }
  };

  return (
    <div className="auth-shell flex min-h-screen items-center justify-center p-6 text-white">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-[32px] border border-slate-700/70 bg-slate-900/40 shadow-[0_30px_80px_rgba(2,6,23,0.75)] backdrop-blur-xl lg:grid-cols-[0.95fr_1.05fr]">
        <div className="relative hidden flex-col justify-between border-r border-slate-700/70 p-8 lg:flex">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(56,189,248,0.18),_transparent_30%),radial-gradient(circle_at_bottom_right,_rgba(37,99,235,0.2),_transparent_25%)]" />
          <div className="relative z-10 flex items-center gap-3">
            <BrandMark className="h-14 w-14" compact />
            <div>
              <div className="brand-word text-3xl font-black tracking-[-0.08em]">ProspectAI</div>
              <p className="text-[10px] uppercase tracking-[0.28em] text-sky-200/80">AI CRM</p>
            </div>
          </div>

          <div className="relative z-10 mt-10 max-w-sm">
            <p className="text-sm uppercase tracking-[0.28em] text-sky-200/80">Nouvelle équipe</p>
            <h1 className="mt-4 text-4xl font-black leading-tight tracking-[-0.05em] text-white">
              Construisez votre pipeline plus vite.
            </h1>
            <p className="mt-4 text-base text-slate-300">
              Créez votre compte et donnez à votre équipe le pouvoir d’identifier les meilleurs prospects dès la première interaction.
            </p>
          </div>

          <div className="relative z-10 mt-10 rounded-2xl border border-slate-700/70 bg-slate-950/40 p-5">
            <p className="text-xs uppercase tracking-[0.2em] text-slate-400">Focus du jour</p>
            <div className="mt-3 flex items-center justify-between">
              <div>
                <div className="text-2xl font-black text-white">9.4/10</div>
                <div className="text-sm text-slate-300">Score de qualification moyen</div>
              </div>
              <div className="rounded-full bg-emerald-500/20 px-2.5 py-1 text-xs font-semibold text-emerald-300">+18%</div>
            </div>
          </div>
        </div>

        <form onSubmit={onSubmit} className="glass-panel w-full p-8 text-white lg:p-10">
          <div className="text-center lg:text-left">
            <p className="text-xs uppercase tracking-[0.3em] text-sky-200/80">Inscription</p>
            <h2 className="mt-3 text-3xl font-black tracking-[-0.06em] text-white">Créer un compte</h2>
          </div>

          <div className="mt-8 space-y-4">
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-200">Nom</label>
              <input className="soft-input" placeholder="Nom complet" value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-200">Email</label>
              <input className="soft-input" placeholder="email@entreprise.com" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-200">Mot de passe</label>
              <input className="soft-input" type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
          </div>

          <button className="primary-button mt-6">S'inscrire</button>

          <div className="mt-4 text-center text-xs text-slate-400">
            <Link to="/conditions-utilisation" className="hover:text-sky-300">
              Conditions d’utilisation
            </Link>
          </div>

          <Link to="/login" className="mt-4 block text-center text-sm font-medium text-sky-300 hover:text-sky-200">
            Retour connexion
          </Link>
        </form>
      </div>
    </div>
  );
}
