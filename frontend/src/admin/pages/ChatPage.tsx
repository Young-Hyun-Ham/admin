// src/admin/pages/ChatPage.tsx

import { Box, Card, CardContent, CardHeader } from '@mui/material';
import { Title, Authenticated } from 'react-admin';
import { useMemo, useRef, useState, useLayoutEffect, useCallback, useEffect } from 'react';
import type { ChatMessage } from '../types';
import ChatMessages from '../components/ChatMessages';
import ChatInput, { type ChatInputRef } from '../components/ChatInput';
import { readToText, streamChatCompletion } from '../api/chatClient';

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(() => ([
    { id: crypto.randomUUID(), role: 'system', content: '당신은 react-admin 프로젝트의 개발을 돕는 조력자입니다.', createdAt: Date.now() }
  ]));
  const [isStreaming, setIsStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const inputRef = useRef<ChatInputRef>(null);

  // ✅ 스크롤 상태
  const scrollRef = useRef<HTMLDivElement>(null); // 스크롤 컨테이너
  const endRef    = useRef<HTMLDivElement>(null); // 맨 아래 앵커
  const [stick, setStick] = useState(true);       // 바닥 고정 여부
  // 컴포넌트 내부
  const [hasVScroll, setHasVScroll] = useState(false);

  const updateHasVScroll = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;

    // 세로 스크롤이 필요하고(내용이 넘침) + 스크롤바가 레이아웃 공간을 실제로 차지하는지(Windows 등)
    const needsScroll = el.scrollHeight > el.clientHeight + 1;
    const occupiesSpace = (el.offsetWidth - el.clientWidth) > 0; // macOS 오버레이 스크롤바는 0
    setHasVScroll(needsScroll && occupiesSpace);
  }, []);
  useLayoutEffect(() => { updateHasVScroll(); }, [updateHasVScroll, messages]);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const ro = new ResizeObserver(updateHasVScroll);
    ro.observe(el);
    return () => ro.disconnect();
  }, [updateHasVScroll]);

  const handleScroll = () => {
    const el = scrollRef.current;
    if (!el) return;
    const nearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 48;
    setStick(nearBottom);
    updateHasVScroll();
  };

  const scrollToBottom = (smooth = false) => {
    if (!stick) return;
    requestAnimationFrame(() => {
      endRef.current?.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'end' });
    });
  };

  useLayoutEffect(() => { scrollToBottom(false); }, []);          // 최초
  useLayoutEffect(() => { scrollToBottom(true); }, [messages]);   // 메시지 변경 시

  const historyForLLM = useMemo(
    () => messages.filter(m => m.role !== 'system').map(m => ({ role: m.role as 'user'|'assistant', content: m.content })),
    [messages]
  );

  const send = async (text: string) => {
    if (isStreaming) return;

    const userMsg: ChatMessage = { id: crypto.randomUUID(), role: 'user', content: text, createdAt: Date.now() };
    setMessages(prev => [...prev, userMsg]);

    const assistantId = crypto.randomUUID();
    setMessages(prev => [...prev, { id: assistantId, role: 'assistant', content: '', createdAt: Date.now() }]);

    setIsStreaming(true);
    const aborter = new AbortController();
    abortRef.current = aborter;

    try {
      const reader = await streamChatCompletion(
        [{ role: 'system', content: 'You are a helpful assistant for a react-admin project.' }, ...historyForLLM, { role: 'user', content: text }],
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
      requestAnimationFrame(() => inputRef.current?.focus());
    }
  };

  return (
    <Authenticated>
      <Title title="GPT-4o-mini Chat" />
      <Card
        sx={{
          height: 'calc(100vh - 64px)',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        <CardHeader title="GPT-4o-mini Chat" />
        <CardContent
          sx={{
            flex: 1,
            p: 0,
            display: 'grid',
            gridTemplateRows: '1fr auto',
            minHeight: 0,
            overflow: 'hidden',
            // ✅ MUI 기본 &:last-child 패딩을 5px로 강제
            '&:last-child': { paddingBottom: '5px' },
          }}
        >
          {/* 스크롤 컨테이너 */}
          <Box
            ref={scrollRef}
            onScroll={handleScroll}
            sx={{ overflowY: 'auto', minHeight: 0, scrollbarGutter: 'stable both-edges', mr: hasVScroll ? '32px' : 0,
    transition: 'margin-right .15s ease',}}
          >
            <Box sx={{ pt: 2, px: 2, pb: 0 }}>
              <ChatMessages messages={messages.filter(m => m.role !== 'system')} />
              <Box ref={endRef} sx={{ height: 1 }} />
            </Box>
          </Box>

          {/* 입력창 래퍼: 아래 여백 0, 위쪽만 간격 */}
          <Box sx={{ px: 2, pt: 2, pb: 0 }}>
            <ChatInput ref={inputRef} onSend={send} disabled={isStreaming} />
          </Box>
        </CardContent>
      </Card>
    </Authenticated>
  );
}
