import ChatWindow from "@/components/ChatWindow";
import UploadPanel from "@/components/UploadPanel";

export default function Home() {
  return (
    <main className="flex h-screen bg-gray-50 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-72 bg-white border-r flex flex-col p-4 gap-6 shrink-0">
        <div>
          <h1 className="text-base font-semibold text-gray-900">
            Clinical Copilot
          </h1>
          <p className="text-xs text-gray-400 mt-0.5">RAG-powered AI assistant</p>
        </div>

        <UploadPanel />

        <div className="text-xs text-gray-400 mt-auto space-y-1">
          <p>Supported: .txt, .pdf</p>
          <p>Backend: localhost:8000</p>
        </div>
      </aside>

      {/* Chat panel */}
      <div className="flex-1 flex flex-col min-w-0">
        <ChatWindow />
      </div>
    </main>
  );
}
