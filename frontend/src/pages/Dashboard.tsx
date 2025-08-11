import { useEffect, useMemo, useState } from 'react';
import { Title, useLogout, useNotify } from 'react-admin';

// 토큰 일부 마스킹 (앞 6, 뒤 4만 보여주기)
const mask = (t: string) => {
  if (!t) return '';
  if (t.length <= 12) return t;
  return `${t.slice(0, 6)}...${t.slice(-4)}`;
};

export default function Dashboard() {
  
  const [token, setToken] = useState<string | null>(null);
  const [type, setType] = useState<string | null>(null);
  const [email, setEmail] = useState<string | null>(null);
  const logout = useLogout();
  const notify = useNotify();

  useEffect(() => {
    setToken(localStorage.getItem('token'));
    setType(localStorage.getItem('type'));
    setEmail(localStorage.getItem('email'));
  }, []);

  const authHeader = useMemo(() => {
    if (!token) return '(없음)';
    return `${type || 'Bearer'} ${mask(token)}`;
  }, [token, type]);

  const copyToken = async () => {
    if (!token) {
      notify('토큰이 없습니다.', { type: 'warning' });
      return;
    }
    await navigator.clipboard.writeText(token);
    notify('토큰을 클립보드에 복사했습니다.', { type: 'info' });
  };

  return (
    <div style={{ padding: 24 }}>
      <Title title="대시보드" />
      <h2 style={{ marginBottom: 8 }}>환영합니다{email ? `, ${email}` : ''} 👋</h2>

      <div style={{ margin: '12px 0' }}>
        <div><b>Authorization 헤더</b></div>
        <code style={{ display: 'inline-block', marginTop: 6 }}>
          {authHeader}
        </code>
      </div>

      <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
        <button onClick={copyToken}>토큰 복사</button>
        <button onClick={() => logout()}>로그아웃</button>
      </div>
    </div>
  );
}
