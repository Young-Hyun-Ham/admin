import { Admin, Resource, ListGuesser } from 'react-admin';
import authProvider from './auth/authProvider';
import LoginPage from './pages/LoginPage';

const App = () => (

  <Admin authProvider={authProvider} loginPage={LoginPage}>
    <Resource name="posts" list={ListGuesser} />
  </Admin>
);

export default App;
