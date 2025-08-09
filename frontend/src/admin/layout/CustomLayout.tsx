import { Layout, AppBar, TitlePortal } from 'react-admin';

const CustomAppBar = () => (
  <AppBar>
    <TitlePortal />
  </AppBar>
);

const CustomLayout = (props: any) => <Layout {...props} appBar={CustomAppBar} />;

export default CustomLayout;
