import { Edit, SimpleForm, TextInput, Toolbar, SaveButton, DeleteButton } from "react-admin";
import { Button, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";

const CustomToolbar = (props: any) => {
  const navigate = useNavigate();

  return (
    <Toolbar {...props} sx={{ display: "flex", justifyContent: "space-between" }}>
      {/* 좌측: List 버튼 */}
      <Button
        variant="outlined"
        color="primary"
        onClick={() => navigate("/board")}
      >
        목록
      </Button>

      {/* 우측: Save + Delete */}
      <Box sx={{ display: "flex", gap: 2 }}>
        <SaveButton />
        <DeleteButton />
      </Box>
    </Toolbar>
  );
};

export const BoardEdit = () => (
  <Edit>
    <SimpleForm toolbar={<CustomToolbar />}>
      <TextInput source="id" disabled />
      <TextInput source="title" label="제목" />
      <TextInput source="body"  label="내용" multiline />
    </SimpleForm>
  </Edit>
);
