import { create } from 'zustand';

interface AuthState {
  isAuthenticated: boolean;
  email: string | null;
  token: string | null;
  login: (email: string, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: !!localStorage.getItem('token'),
  email: localStorage.getItem('email'),
  token: localStorage.getItem('token'),
  login: async (email, password) => {
    const response = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
        throw new Error("로그인 실패");
    }

    const { token, email: name } = await response.json();
    useAuthStore.getState().login(name, token);
  },
  logout: () => {
    localStorage.removeItem('email');
    localStorage.removeItem('token');
    set({ isAuthenticated: false, email: null, token: null });
  },
}));
