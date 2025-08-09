// src/admin/api/chatClient.ts

// 스트리밍 응답을 텍스트로 이어 붙이는 유틸리티
export async function streamChatCompletion(
  messages: { role: 'system' | 'user' | 'assistant'; content: string }[],
  signal?: AbortSignal
): Promise<ReadableStreamDefaultReader<Uint8Array>> {
  console.log("content ================>", JSON.stringify({ messages }));
  const res = await fetch('http://127.0.0.1:8000/chat/stream', {
    method: 'POST',
    body: JSON.stringify({ messages }),
    headers: { 'Content-Type': 'application/json' },
    signal
  });

  if (!res.ok || !res.body) {
    throw new Error(`Chat stream failed: ${res.status}`);
  }
  return res.body.getReader();
}

// export async function readToText(
//   reader: ReadableStreamDefaultReader<Uint8Array>,
//   onChunk: (text: string) => void
// ) {
//   const decoder = new TextDecoder('utf-8');
//   let done = false;
//   while (!done) {
//     const result = await reader.read();
//     done = result.done || false;
//     const chunk = result.value ? decoder.decode(result.value, { stream: true }) : '';
//     if (chunk) onChunk(chunk);
//   }
// }

export async function readToText(
  reader: ReadableStreamDefaultReader<Uint8Array>,
  onChunk: (text: string) => void
) {
  const decoder = new TextDecoder();
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      if (value) onChunk(decoder.decode(value, { stream: true }));
    }
  } finally {
    reader.releaseLock();
  }
}