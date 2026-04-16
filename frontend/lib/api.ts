const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface Source {
  content: string;
  score: number;
  metadata: Record<string, unknown>;
}

export interface ChatResponse {
  message: string;
  sources: Source[];
  session_id?: string;
}

export interface IngestResponse {
  filename: string;
  status: string;
  chunks_stored: number;
  message: string;
}

export async function sendMessage(
  message: string,
  sessionId?: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  if (!res.ok) throw new Error(`Chat request failed: ${res.status}`);
  return res.json();
}

export async function uploadDocument(file: File): Promise<IngestResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_URL}/api/ingest`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
  return res.json();
}

export async function checkHealth(): Promise<{ status: string }> {
  const res = await fetch(`${API_URL}/api/health`);
  if (!res.ok) throw new Error("Backend unreachable");
  return res.json();
}
