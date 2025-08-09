import { useMediaQuery, type Theme, Box, Stack } from "@mui/material";
import {
  List,
  Datagrid,
  TextField,
  DeleteButton,
  SimpleList,
  FunctionField,
} from "react-admin";
import { CustomPagination } from "./../components/CustomPagination";
import { Button, Pagination } from 'react-admin';
import EditIcon from '@mui/icons-material/Edit';
import { useNavigate } from 'react-router-dom';

export const BoardList = () => {
  const navigate = useNavigate();

  const isSmall = useMediaQuery<Theme>((theme) => theme.breakpoints.down("sm"));
  return (
    <List 
      perPage={10}
      pagination={
        /*<CustomPagination />*/
        <Pagination rowsPerPageOptions={[5, 10, 25, 50]} />
      }
    >
      {isSmall ? (
        <>
          {/* 헤더 */}
          <Box px={2} py={1} sx={{ display: "flex", fontWeight: 600, color: "text.secondary" }}>
            <Box sx={{ width: 56 }}>No</Box>
            <Box sx={{ flex: 1 }}>Title</Box>
          </Box>

          <SimpleList
              primaryText={(record) => (
                <Box sx={{ display: "flex", alignItems: "center" }}>
                  <Box sx={{ width: 56 }}>{record.id}</Box>
                  <Box sx={{ flex: 1, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                    {record.title}
                  </Box>
                </Box>
              )}
              secondaryText={() => null}
          />
        </>
      ) : (
        <Datagrid rowClick="edit"
          // 컬럼 폭 고정용 class에 스타일 적용
          sx={{
            "& .column-id": { width: "60px", maxWidth: "60px" },
            "& .column-title": { width: "200px", maxWidth: "200px" },
            "& .column-content": { width: "500px", maxWidth: "500px" },
            "& .col-actions": { width: 10, minWidth: 10, maxWidth: 90 },
            // 필요하면 버튼 아이콘/텍스트 간격도 축소
            "& .col-actions .MuiButton-root": { minWidth: 0, padding: "1px 1px" },
          }}
        >
          <TextField source="id"   label="ID" />
          <TextField source="title" label="제목" />
          <TextField source="body"  label="내용" />
          {/* 액션 컬럼을 FunctionField로 묶어서 고정폭 + 버튼 크기 제어 */}
          <FunctionField
            label="Actions"
            headerClassName="col-actions"
            cellClassName="col-actions"
            render={(record) => (
              <Stack direction="row" spacing={1} justifyContent="flex-end">
                {/* 크기 축소: size="small", 라벨 없애고 아이콘만 쓰고 싶으면 label={false} */}
                <Button
                  label=""
                  startIcon={<EditIcon />}
                  onClick={() => navigate(`/board/${record.id}`)}
                />
                <DeleteButton record={record} size="small" label={false} />
              </Stack>
            )}
          />
        </Datagrid>
      )}
    </List>
  );
};
