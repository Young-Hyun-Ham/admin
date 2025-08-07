import type { AuthProvider } from 'react-admin';
import { useAuthStore } from '../store/authStore';

const authProvider: AuthProvider = {
  login: async ({ email, password }) => {
    const response = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
        throw new Error("로그인 실패");
    }

    const { token, email: name } = await response.json();
    localStorage.setItem("token", token);
    localStorage.setItem("email", name);
    useAuthStore.getState().login(name, token);
    },
  logout: () => {
    useAuthStore.getState().logout();
    return Promise.resolve();
  },
  checkAuth: () => {
    console.log('[authProvider] checkAuth: token =qqqq');
    const token = useAuthStore.getState().token;
    console.log('[authProvider] checkAuth: token =', token);
    return token ? Promise.resolve() : Promise.reject();
  },
  checkError: () => Promise.resolve(),
  getPermissions: () => Promise.resolve(),
  getIdentity: () => {
    const email = useAuthStore.getState().email;
    return Promise.resolve({ id: email || '', fullName: email || '' });
  },
};

export default authProvider;
