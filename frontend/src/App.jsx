import { useState } from "react";

const API = "http://localhost:8000/api";

export default function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [q, setQ] = useState("");
  const [resp, setResp] = useState(null);
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    setStatus("Ingesting…");
    const r = await fetch(`${API}/ingest`, { method: "POST", body: fd });
    const d = await r.json();
    setStatus(`Indexed ${d.chunks} chunks (${d.filename})`);
  };

  const ask = async () => {
    setLoading(true); setResp(null);
    const r = await fetch(`${API}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q, mode: "auto" }),
    });
    setResp(await r.json());
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 720, margin: "40px auto", fontFamily: "system-ui" }}>
      <h1>PaperMind</h1>
      <section style={{ marginBottom: 24 }}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={upload}>Ingest</button>
        <p>{status}</p>
      </section>
      <section>
        <textarea
          rows={3} style={{ width: "100%" }} value={q}
          placeholder="Ask a question, request a summary, or extract fields…"
          onChange={(e) => setQ(e.target.value)}
        />
        <button onClick={ask} disabled={loading || !q}>
          {loading ? "Thinking…" : "Ask"}
        </button>
      </section>
      {resp && (
        <section style={{ marginTop: 24 }}>
          <p><b>Intent:</b> {resp.intent} · <b>Grounded:</b> {String(resp.grounded)}</p>
          <div style={{ whiteSpace: "pre-wrap", background: "#f5f5f5", padding: 16 }}>
            {resp.answer}
          </div>
          <details style={{ marginTop: 12 }}>
            <summary>Sources ({resp.sources.length})</summary>
            {resp.sources.map((s, i) => (
              <p key={i} style={{ fontSize: 13 }}>
                <b>{s.score.toFixed(3)}</b> · {s.text.slice(0, 160)}…
              </p>
            ))}
          </details>
        </section>
      )}
    </div>
  );
}