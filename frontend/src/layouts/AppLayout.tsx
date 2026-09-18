import { NavLink, Outlet, useNavigate } from "react-router-dom";
import {
  Activity,
  BarChart3,
  Bell,
  LayoutDashboard,
  LogOut,
  Search,
  Settings,
  Target,
  Users,
  KanbanSquare,
  CalendarClock,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useState } from "react";
import BrandMark from "../components/BrandMark";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/prospects", label: "Prospects", icon: Target },
  { to: "/pipeline", label: "Pipeline", icon: KanbanSquare },
  { to: "/prospecting", label: "Prospection", icon: Search },
  { to: "/follow-ups", label: "Relances", icon: CalendarClock },
  { to: "/activities", label: "Activités", icon: Activity },
  { to: "/reports", label: "Rapports", icon: BarChart3 },
];

export default function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [query, setQuery] = useState("");

  return (
    <div className="min-h-screen bg-slate-50 lg:flex">
      <aside
        className="w-full border-b border-slate-200 bg-slate-950 text-white lg:min-h-screen lg:w-64 lg:border-b-0 flex-shrink-0"
      >
        <div className="px-4 py-5 flex flex-col lg:flex-row items-center gap-4">
          <BrandMark className="h-12 w-12" compact />
          <div className="hidden lg:block">
            <p className="text-[10px] uppercase tracking-[0.28em] text-blue-300">AI CRM</p>
            <h1 className="text-lg font-black tracking-tight text-white">ProspectAI</h1>
          </div>
        </div>
        <nav className="mt-6 flex flex-col lg:flex-row gap-1 overflow-x-auto px-3 pb-3 lg:flex-col lg:overflow-visible">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === "/"}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition-colors ${isActive
                  ? "bg-sky-500/20 text-sky-300 border-sky-500/30"
                  : "text-slate-300 hover:bg-slate-800/50 hover:text-white"}`
              }
            >
              <link.icon size={18} className="text-sky-300" />
              <span className="hidden lg inline">{link.label}</span>
            </NavLink>
          ))}
          {user?.role === "ADMIN" && (
            <NavLink
              to="/users"
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition-colors ${isActive
                  ? "bg-sky-500/20 text-sky-300 border-sky-500/30"
                  : "text-slate-300 hover:bg-slate-800/50 hover:text-white"}`
              }
            >
              <Users size={18} className="text-sky-300" />
              <span className="hidden lg inline">Utilisateurs</span>
            </NavLink>
          )}
          <NavLink
            to="/settings"
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition-colors ${isActive
                ? "bg-sky-500/20 text-sky-300 border-sky-500/30"
                : "text-slate-300 hover:bg-slate-800/50 hover:text-white"}`
            }
          >
            <Settings size={18} className="text-sky-300" />
            <span className="hidden lg inline">Paramètres</span>
          </NavLink>
        </nav>
      </aside>
      <div className="flex-1">
        <header className="w-full lg:w-auto border-b border-slate-200 bg-slate-950/50 backdrop-blur-sm px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
          <form
            className="relative w-full max-w-md"
            onSubmit={(event) => {
              event.preventDefault();
              navigate(`/prospects?search=${encodeURIComponent(query)}`);
            }}
          >
            <Search className="absolute left-3 top-2.5 text-slate-400" size={18} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Rechercher un prospect…"
              className="w-full rounded-xl border border-slate-400 bg-slate-900/50 py-2 pl-10 pr-3 text-sm outline-none focus:border-sky-400"
            />
          </form>
          <div className="flex items-center gap-3">
            <button
              className="rounded-full bg-sky-500/20 p-2 text-sky-300 hover:bg-sky-500/30 transition-colors"
              aria-label="Notifications"
            >
              <Bell size={18} />
            </button>
            <div className="hidden lg:flex items-center gap-2">
              <p className="text-sm font-semibold text-slate-200">{user?.name}</p>
              <p className="text-xs text-slate-400">{user?.role}</p>
            </div>
            <button
              onClick={() => logout().then(() => navigate("/login"))}
              className="rounded-xl border border-slate-500/30 bg-slate-900/50 px-3 py-2 text-sm text-slate-400 hover:bg-slate-800/50 transition-colors"
              aria-label="Déconnexion"
            >
              <LogOut size={18} />
            </button>
          </div>
        </header>
        <main className="lg:w-full p-4 sm:p-8 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
