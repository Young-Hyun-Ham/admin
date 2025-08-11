import type { AuthProvider } from 'react-admin';
import { useAuthStore } from '../store/authStore';
import { api } from '../api/axios';
import type { AxiosResponse } from 'axios';
import { jwtDecode } from 'jwt-decode';

type Claims = { sub: string; role?: 'admin' | 'user'; [k: string]: any };

interface resLogin extends AxiosResponse {
  data: {access_token: string, token_type: string}
};

const authProvider: AuthProvider = {
  login: async ({ email, password }) => {
    const response: resLogin = await api.post("/v1/api/auth/login", { email, password })

    if (response.status !== 200) {
      throw new Error("로그인 실패");
    }

    const { access_token, token_type } = await response.data;
    localStorage.setItem("token", access_token);
    localStorage.setItem("type", token_type);
    localStorage.setItem("email", email);
    useAuthStore.setState({token: access_token, isAuthenticated: true})
  },
  logout: () => {
    useAuthStore.getState().logout();
    return Promise.resolve();
  },
  checkAuth: () => {
    const token = useAuthStore.getState().token;
    return token ? Promise.resolve() : Promise.reject();
  },
  checkError: () => Promise.resolve(),
  // 권한 값 반환
  async getPermissions() {
    const t = localStorage.getItem("token");
    if (!t) return 'guest';
    const { roles } = jwtDecode<Claims>(t);
    return roles.some((role: any) => role === "admin") ? "admin" : "user"
  },
  getIdentity: () => {
    const email = useAuthStore.getState().email;
    return Promise.resolve({ id: email || '', fullName: email || '' });
  },
};

export default authProvider;
