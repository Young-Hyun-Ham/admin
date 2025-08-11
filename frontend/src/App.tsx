import { Admin, CustomRoutes, Resource, usePermissions, type ListProps} from 'react-admin';

// 1. 만들어 둔 Provider들을 import 합니다.
import authProvider from './auth/authProvider';
import dataProvider from './auth/dataProvider';

// 예시: pages 디렉토리에 게시물(Post) 관련 컴포넌트가 있다고 가정
import { BoardList, BoardEdit, BoardCreate } from './pages/board';
import Dashboard from './pages/Dashboard'; // 대쉬보드(메인화면)
import LoginPage from './pages/LoginPage'; // 내가 만든 로그인 페이지
import ChatPage from './admin/pages/ChatPage';

type Perm = 'admin' | 'user' | 'guest';

const App = () => (
    // 2. <Admin> 컴포넌트의 props로 전달하여 설정합니다.
    <Admin
        authProvider={authProvider}
        dataProvider={dataProvider}
        loginPage={LoginPage} // 커스텀 로그인 페이지 적용 <- 제거시 react-admin이 제공한 로그인 화면으로 이동
        dashboard={Dashboard}
    >
        {(permissions: Perm) => (
        <>
            <Resource
                name="board"
                list={(props: ListProps) => (
                    <BoardList {...props} permissions={permissions} />
                )}
                edit={BoardEdit}
                create={BoardCreate}
            />
            {(permissions !== 'user' && permissions !== undefined ) && (
            <Resource
              name="chat"
              list={ChatPage}
              options={{ label: 'AI 채팅' }}
            />
          )}
        </>
      )}
        {/* <CustomRoutes>
            <Route path="/" element={<ChatPage />} />
        </CustomRoutes> */}
    </Admin>
);

export default App;
