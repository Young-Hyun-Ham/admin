import { Box, Card, CardContent, CardHeader } from '@mui/material';
import { Title, Authenticated } from 'react-admin';
import { useMemo, useRef, useState } from 'react';
import type { ChatMessage } from '../types';
import ChatMessages from '../components/ChatMessages';
import ChatInput from '../components/ChatInput';
import { readToText, streamChatCompletion } from '../api/chatClient';

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(() => ([
    {
      id: crypto.randomUUID(),
      role: 'system',
      content: '당신은 react-admin 프로젝트의 개발을 돕는 조력자입니다.',
      createdAt: Date.now()
    }
  ]));
  const [isStreaming, setIsStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const historyForLLM = useMemo(
    () => messages
      .filter(m => m.role !== 'system') // 초기 system은 유지해도 OK. 필요시 포함
      .map(m => ({ role: m.role as 'user' | 'assistant', content: m.content })),
    [messages]
  );

  const send = async (text: string) => {
    if (isStreaming) return;

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      createdAt: Date.now()
    };
    setMessages(prev => [...prev, userMsg]);

    // 어시스턴트 메시지 자리 미리 생성(스트림으로 덧붙임)
    const assistantId = crypto.randomUUID();
    setMessages(prev => [...prev, { id: assistantId, role: 'assistant', content: '', createdAt: Date.now() }]);

    setIsStreaming(true);
    const aborter = new AbortController();
    abortRef.current = aborter;

    try {
      const reader = await streamChatCompletion(
        [
          { role: 'system', content: 'You are a helpful assistant for a react-admin project.' },
          ...historyForLLM,
          { role: 'user', content: text }
        ],
        aborter.signal
      );

      await readToText(reader, (chunk) => {
        setMessages(prev => prev.map(m => m.id === assistantId ? { ...m, content: m.content + chunk } : m));
      });
    } catch (err) {
      setMessages(prev => prev.map(m => m.id === assistantId ? { ...m, content: `⚠️ 오류: ${(err as Error).message}` } : m));
    } finally {
      setIsStreaming(false);
      abortRef.current = null;
    }
  };

  return (
    <Authenticated>
      <Title title="GPT-4o-mini Chat" />
      <Card sx={{ 
        height: 'calc(100vh - 64px)',
        display: 'flex', 
        flexDirection: 'column' 
      }}>
        <CardHeader title="GPT-4o-mini Chat" />
        
        <CardContent sx={{
          flex: 1,
          position: 'relative',
          p: 0,
          overflow: 'hidden',
        }}>

          {/* 1. 바깥쪽 Box (스크롤 컨테이너) */}
          {/* 이 요소가 스크롤을 담당합니다. 여기에는 패딩이 없습니다. */}
          <Box sx={{
            position: 'absolute',
            top: 0, left: 0, right: 0, bottom: 0,
            overflowY: 'auto', // 내용(안쪽 Box)이 넘칠 때만 스크롤이 생깁니다.
          }}>
            
            {/* 2. 안쪽 Box (콘텐츠 + 하단 여백) */}
            {/* 이 요소는 메시지를 담고 하단 여백을 만드는 역할만 합니다. */}
            <Box sx={{
              pt: 2, px: 2,
              //pb: '200px', // 입력창에 가려질 부분을 위한 충분한 하단 여백
            }}>
              <ChatMessages messages={messages.filter(m => m.role !== 'system')} />
            </Box>

          </Box>

          {/* 3. 입력창 (별도 레이어) */}
          <Box sx={{
            position: 'absolute',
            bottom: 0, left: 0, right: 0,
            pointerEvents: 'auto',
          }}>
            <ChatInput onSend={send} disabled={isStreaming} />
          </Box>
            
        </CardContent>
      </Card>
    </Authenticated>
  );
}
