import { FormEvent, useState } from "react";
import api from "../services/api";
import { useAsync } from "../hooks/useAsync";
import { User } from "../types";
import { Loader, ErrorState } from "../components/States";
import { useToast } from "../context/ToastContext";
import Modal from "../components/Modal";

export default function UsersPage() {
  const { notify } = useToast();
  const { data, loading, error, reload } = useAsync<User[]>(async () => (await api.get("/users/")).data, []);
  const [open, setOpen] = useState(false);

  const createUser = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api.post("/users/", {
      name: form.get("name"),
      email: form.get("email"),
      password: form.get("password"),
      role: form.get("role"),
    });
    notify("Utilisateur créé");
    setOpen(false);
    reload();
  };

  const patch = async (id: number, payload: Partial<User> & { password?: string }) => {
    await api.patch(`/users/${id}`, payload);
    notify("Utilisateur mis à jour");
    reload();
  };

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Utilisateurs</h2>
        <button onClick={() => setOpen(true)} className="rounded-xl bg-blue-600 px-4 py-2 text-sm text-white">
          Créer
        </button>
      </div>
      <div className="card divide-y">
        {data?.map((user) => (
          <div key={user.id} className="flex flex-wrap items-center justify-between gap-3 px-4 py-3">
            <div>
              <p className="font-medium">{user.name}</p>
              <p className="text-sm text-slate-500">{user.email}</p>
            </div>
            <div className="flex gap-2">
              <select className="rounded-lg border px-2 py-1 text-sm" value={user.role} onChange={(e) => patch(user.id, { role: e.target.value as User["role"] })}>
                <option>ADMIN</option>
                <option>MANAGER</option>
                <option>COMMERCIAL</option>
              </select>
              <button onClick={() => patch(user.id, { is_active: !user.is_active })} className="rounded-lg border px-3 py-1 text-sm">
                {user.is_active ? "Désactiver" : "Activer"}
              </button>
            </div>
          </div>
        ))}
      </div>
      <Modal open={open} title="Nouvel utilisateur" onClose={() => setOpen(false)}>
        <form className="space-y-3" onSubmit={createUser}>
          <input name="name" placeholder="Nom" className="w-full rounded-xl border px-3 py-2" required />
          <input name="email" type="email" placeholder="Email" className="w-full rounded-xl border px-3 py-2" required />
          <input name="password" type="password" placeholder="Mot de passe" className="w-full rounded-xl border px-3 py-2" required />
          <select name="role" className="w-full rounded-xl border px-3 py-2">
            <option>COMMERCIAL</option>
            <option>MANAGER</option>
            <option>ADMIN</option>
          </select>
          <button className="w-full rounded-xl bg-blue-600 py-2 text-white">Créer</button>
        </form>
      </Modal>
    </div>
  );
}
