// src/components/CustomPagination.tsx
import { Box, FormControl, Select, MenuItem, Pagination as MuiPagination } from "@mui/material";
import { useListContext } from "react-admin";

const ROWS_PER_PAGE_OPTIONS = [2, 5, 10, 25, 50];

export const CustomPagination = () => {
  const { page, perPage, total, setPage, setPerPage } = useListContext();
  if (!total || total < 0) return null;

  const pageCount = Math.max(1, Math.ceil(total / perPage));

  // 버튼/셀렉트/좌우 여백의 공통 사이즈
  const controlSize = 32;   // 32~36 선호
  const barHeight   = 40;   // 하단 바 고정 높이
  const fontSize    = "0.875rem";

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        height: barHeight,     // ★ 바 높이 고정
        px: 1,                 // 상하 패딩 제거해서 라인 맞춤
        mt: "10px",            // ★ 게시판과의 간격
      }}
    >
      {/* 왼쪽 여백 (우측 Select와 동일 폭) */}
      <Box sx={{ flex: "none", minWidth: controlSize }} />

      {/* 가운데 Pagination */}
      <Box sx={{ flex: "none" }}>
        <MuiPagination
          count={pageCount}
          page={page}
          onChange={(_, v) => setPage(v)}
          size="small"
          shape="rounded"
          color="primary"
          siblingCount={1}
          boundaryCount={1}
          showFirstButton
          showLastButton
          sx={{
            // 버튼 높이/폭 통일 + 위아래 마진 제거로 수직 정렬 정확히
            "& .MuiPaginationItem-root": {
              width: controlSize,
              height: controlSize,
              minWidth: controlSize,
              fontSize,
              m: 0,                 // 위아래 여백 제거
            },
          }}
        />
      </Box>

      {/* 우측 Rows per page (outlined로 밑줄 제거 + 높이/폭 통일) */}
      <Box sx={{ flex: "none", minWidth: controlSize, display: "flex", justifyContent: "flex-end" }}>
        <FormControl size="small" variant="outlined" sx={{ width: 60 }}>
          <Select
            value={perPage}
            onChange={(e) => {
              setPerPage(Number(e.target.value));
              setPage(1);
            }}
            displayEmpty
            inputProps={{ "aria-label": "Rows per page" }}
            sx={{
              height: controlSize,
              fontSize,
              "& .MuiSelect-select": {
                p: 0,
                textAlign: "center",
                lineHeight: `${controlSize}px`,
              },
              "& .MuiOutlinedInput-notchedOutline legend": { display: "none" }, // 라벨 공간 제거
              "& .MuiSelect-icon": { right: 2 },
            }}
          >
            {ROWS_PER_PAGE_OPTIONS.map((opt) => (
              <MenuItem key={opt} value={opt} sx={{ minHeight: controlSize, fontSize, p: 0, textAlign: "center" }}>
                {opt}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
    </Box>
  );
};
