"use client";
import { useState } from "react";
import { uploadDocument } from "@/lib/api";

type UploadStatus = "idle" | "uploading" | "success" | "error";

export default function UploadPanel() {
  const [status, setStatus] = useState<UploadStatus>("idle");
  const [message, setMessage] = useState<string>("");

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setStatus("uploading");
    setMessage("");

    try {
      const res = await uploadDocument(file);
      setStatus("success");
      setMessage(`✓ ${res.filename} — ${res.message}`);
    } catch {
      setStatus("error");
      setMessage("Upload failed. Make sure the backend is running.");
    }

    // Reset input so the same file can be re-uploaded
    e.target.value = "";
  };

  return (
    <div className="border border-dashed border-gray-300 rounded-xl p-4">
      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-3">
        Upload Clinical Note
      </p>
      <label
        className={`cursor-pointer flex items-center justify-center gap-2 bg-white border border-gray-300 rounded-lg px-4 py-2 text-sm transition hover:bg-gray-50 ${
          status === "uploading" ? "opacity-50 pointer-events-none" : ""
        }`}
      >
        <span>{status === "uploading" ? "Uploading..." : "Choose .txt or .pdf"}</span>
        <input
          type="file"
          accept=".txt,.pdf"
          className="hidden"
          onChange={handleUpload}
          disabled={status === "uploading"}
        />
      </label>

      {message && (
        <p
          className={`mt-2 text-xs leading-snug ${
            status === "error" ? "text-red-500" : "text-gray-500"
          }`}
        >
          {message}
        </p>
      )}
    </div>
  );
}
