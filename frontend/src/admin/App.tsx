import { Admin, CustomRoutes, Resource } from 'react-admin';
import { Route } from 'react-router-dom';
import dataProvider from './dataProvider';
import CustomLayout from './layout/CustomLayout';
import ChatPage from './pages/ChatPage';

export default function App() {
  return (
    <Admin
      dataProvider={dataProvider}
      layout={CustomLayout}
      title="GPT-4o-mini Chat"
    >
      {/* 리소스는 없어도 되고, 필요시 추가 */}
      <Resource name="placeholder" />
      <CustomRoutes>
        <Route path="/" element={<ChatPage />} />
      </CustomRoutes>
    </Admin>
  );
}
