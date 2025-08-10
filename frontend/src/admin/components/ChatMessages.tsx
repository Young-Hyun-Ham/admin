// src/admin/components/ChatMessages.tsx

import { Box, Paper, Typography } from '@mui/material';
import type { ChatMessage } from '../types';

type Props = {
  messages: ChatMessage[];
};

export default function ChatMessages({ messages }: Props) {
  return (
    <Box sx={{ p: 2, height: 'calc(100vh - 240px)', overflowY: 'auto' }}>
      {messages.map(m => (
        <Box key={m.id} sx={{ display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start', mb: 1.5 }}>
          <Paper
            elevation={1}
            sx={{
              p: 1.5,
              maxWidth: '70%',
              bgcolor: m.role === 'user' ? 'primary.main' : 'background.paper',
              color: m.role === 'user' ? 'primary.contrastText' : 'text.primary',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word'
            }}
          >
            <Typography variant="body2">{m.content}</Typography>
          </Paper>
        </Box>
      ))}
    </Box>
  );
}
