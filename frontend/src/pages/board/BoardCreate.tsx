import { Create, SimpleForm, TextInput } from 'react-admin';

export const BoardCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="title" label="제목" />
      <TextInput source="body"  label="내용" multiline />
    </SimpleForm>
  </Create>
);
