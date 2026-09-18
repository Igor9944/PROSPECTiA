import { createContext, useContext, useEffect, useMemo, useState, ReactNode } from "react";
import api from "../services/api";
import { User } from "../types";

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const loadMe = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }
    try {
      const { data } = await api.get("/auth/me");
      setUser(data);
    } catch {
      localStorage.removeItem("token");
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMe();
  }, []);

  const value = useMemo(
    () => ({
      user,
      loading,
      login: async (email: string, password: string) => {
        const { data } = await api.post("/auth/login", { email, password });
        localStorage.setItem("token", data.access_token);
        const me = await api.get("/auth/me");
        setUser(me.data);
      },
      register: async (name: string, email: string, password: string) => {
        await api.post("/auth/register", { name, email, password, role: "COMMERCIAL" });
        const { data } = await api.post("/auth/login", { email, password });
        localStorage.setItem("token", data.access_token);
        const me = await api.get("/auth/me");
        setUser(me.data);
      },
      logout: async () => {
        try {
          await api.post("/auth/logout");
        } finally {
          localStorage.removeItem("token");
          setUser(null);
        }
      },
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("AuthContext manquant");
  return context;
}
