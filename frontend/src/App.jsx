import { useRef, useState } from "react";
import "./App.css";

const API_BASE =
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:8080"
    : "https://cloudops-ai-xf6sboo7fa-uc.a.run.app";

const DEMO_USER_ID = "ronak-e2e";

const suggestions = [
  "Show my customers",
  "Analyze enterprise data",
  "Search the knowledge base",
  "Analyze a document",
];

const initialMessages = [
  {
    id: 1,
    role: "assistant",
    text: "Hello Ronak. I'm CloudOps AI — your enterprise AI assistant. Ask me about your data, enterprise knowledge, documents, or workflows.",
  },
];

async function createSession(sessionId) {
  const response = await fetch(
    `${API_BASE}/apps/agents/users/${DEMO_USER_ID}/sessions/${sessionId}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: "{}",
    }
  );

  if (!response.ok) {
    throw new Error(`Session creation failed (${response.status})`);
  }

  return response.json();
}

async function runAgent(sessionId, message) {
  const response = await fetch(`${API_BASE}/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      appName: "agents",
      userId: DEMO_USER_ID,
      sessionId,
      newMessage: {
        role: "user",
        parts: [
          {
            text: message,
          },
        ],
      },
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `CloudOps AI request failed (${response.status}): ${errorText}`
    );
  }

  return response.json();
}

function extractAssistantText(events) {
  if (!Array.isArray(events)) {
    return "The agent returned an unexpected response format.";
  }

  const assistantEvents = events.filter(
    (event) =>
      event?.author &&
      event.author !== "user" &&
      event?.content?.parts
  );

  for (let index = assistantEvents.length - 1; index >= 0; index -= 1) {
    const parts = assistantEvents[index].content.parts;

    const textParts = parts
      .filter((part) => typeof part?.text === "string")
      .map((part) => part.text.trim())
      .filter(Boolean);

    if (textParts.length > 0) {
      return textParts.join("\n");
    }
  }

  return "CloudOps AI completed the request, but no text response was returned.";
}

function renderAssistantText(text) {
  const cleanText = text
    .replace(/\*\*/g, "")
    .replace(/\r/g, "")
    .trim();

  const renderCustomerCards = (intro, customers) => (
    <div className="structured-response">
      {intro && <div className="response-intro">{intro}</div>}

      <div className="customer-list">
        {customers.map((customer, index) => (
          <div
            className="customer-card"
            key={`${customer.id || "customer"}-${index}`}
          >
            <div className="customer-card-header">
              <div>
                <div className="customer-name">
                  {customer.name || "Customer"}
                </div>

                <div className="customer-email">
                  {customer.email}
                </div>
              </div>

              {customer.id && (
                <div className="customer-id">
                  #{customer.id}
                </div>
              )}
            </div>

            <div className="customer-meta">
              {customer.region && <span>{customer.region}</span>}

              {customer.region && customer.createdAt && (
                <span>•</span>
              )}

              {customer.createdAt && (
                <span>{customer.createdAt}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // ---------------------------------------------------------
  // FORMAT 1: Markdown table
  // ---------------------------------------------------------

  const tableLines = cleanText
    .split("\n")
    .map((line) => line.trim())
    .filter(
      (line) =>
        line.startsWith("|") &&
        line.endsWith("|")
    );

  const isCustomerTable =
    tableLines.length >= 3 &&
    /customer_id/i.test(tableLines[0]) &&
    /customer_name/i.test(tableLines[0]);

  if (isCustomerTable) {
    const headers = tableLines[0]
      .split("|")
      .map((item) => item.trim().toLowerCase())
      .filter(Boolean);

    const rows = tableLines
      .slice(2)
      .map((line) =>
        line
          .split("|")
          .map((item) => item.trim())
          .filter(Boolean)
      )
      .filter((row) => row.length >= headers.length);

    const getValue = (row, name) => {
      const index = headers.indexOf(name);
      return index >= 0 ? row[index] || "" : "";
    };

    const customers = rows.map((row) => ({
      id: getValue(row, "customer_id"),
      name: getValue(row, "customer_name"),
      email: getValue(row, "email"),
      region: getValue(row, "region"),
      createdAt: getValue(row, "created_at"),
    }));

    return renderCustomerCards(
      "Here are your customers:",
      customers
    );
  }

  // ---------------------------------------------------------
  // FORMAT 2: Customer ID / Name / Email / Region / Created At
  // ---------------------------------------------------------

  const labeledPattern =
    /Customer ID:\s*(\d+)\s*,\s*Name:\s*([^,\n]+)\s*,\s*Email:\s*([^,\n]+)\s*,\s*Region:\s*([^,\n]+)\s*,\s*Created At:\s*([^•\n]+)/gi;

  const labeledCustomers = [
    ...cleanText.matchAll(labeledPattern),
  ].map((match) => ({
    id: match[1]?.trim() || "",
    name: match[2]?.trim() || "",
    email: match[3]?.trim() || "",
    region: match[4]?.trim() || "",
    createdAt: match[5]?.trim() || "",
  }));

  if (labeledCustomers.length > 0) {
    return renderCustomerCards(
      "Here are your customers:",
      labeledCustomers
    );
  }

  // ---------------------------------------------------------
  // FORMAT 3: customer_id / customer_name / email / region
  // ---------------------------------------------------------

  const keyValuePattern =
    /customer_id:\s*(\d+)\s+customer_name:\s*([^\n]+?)\s+email:\s*([^\n]+?)\s+region:\s*([^\n]+?)\s+created_at:\s*([^\n]+?)(?=\s+customer_id:|$)/gi;

  const keyValueCustomers = [
    ...cleanText.matchAll(keyValuePattern),
  ].map((match) => ({
    id: match[1]?.trim() || "",
    name: match[2]?.trim() || "",
    email: match[3]?.trim() || "",
    region: match[4]?.trim() || "",
    createdAt: match[5]?.trim() || "",
  }));

  if (keyValueCustomers.length > 0) {
    return renderCustomerCards(
      "Here are your customers:",
      keyValueCustomers
    );
  }

  // ---------------------------------------------------------
  // Normal AI response
  // ---------------------------------------------------------

  const normalized = cleanText
    .replace(/^\s*[•*]\s*/gm, "")
    .replace(/\n\s*\n/g, "\n");

  return normalized.split("\n").map((line, lineIndex) => (
    <div key={lineIndex} className="response-line">
      {line}
    </div>
  ));
}

function App() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState("");
  const [activeSection, setActiveSection] = useState("Overview");
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const sendMessage = async (value = input) => {
    const text = value.trim();

    if (!text || loading) {
      return;
    }

    const userMessage = {
      id: `${Date.now()}-user`,
      role: "user",
      text,
    };

    setMessages((current) => [...current, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const sessionId = `frontend-${Date.now()}`;

      await createSession(sessionId);

      const result = await runAgent(sessionId, text);

      const assistantText = extractAssistantText(result);

      setMessages((current) => [
        ...current,
        {
          id: `${Date.now()}-assistant`,
          role: "assistant",
          text: assistantText,
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: `${Date.now()}-error`,
          role: "assistant",
          text: `I couldn't reach the CloudOps AI backend.\n\n${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage();
  };

  const analyzeImage = async (file) => {
    if (!file || loading) return;

    const allowedTypes = ["image/png", "image/jpeg", "image/webp"];
    const maxSize = 10 * 1024 * 1024;

    if (!allowedTypes.includes(file.type)) {
      setMessages((current) => [
        ...current,
        {
          id: `${Date.now()}-error`,
          role: "assistant",
          text: "Please upload a PNG, JPG, JPEG, or WEBP image.",
        },
      ]);
      return;
    }

    if (file.size > maxSize) {
      setMessages((current) => [
        ...current,
        {
          id: `${Date.now()}-error`,
          role: "assistant",
          text: "The image is too large. Please upload an image smaller than 10 MB.",
        },
      ]);
      return;
    }

    const question =
      input.trim() ||
      "Analyze this image and describe the important information visible in it.";

    setMessages((current) => [
      ...current,
      {
        id: `${Date.now()}-user`,
        role: "user",
        text: `📎 ${file.name}\n${question}`,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("question", question);

      const response = await fetch(`${API_BASE}/multimodal/analyze`, {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(
          result.detail ||
            result.error ||
            `Image analysis failed (${response.status})`
        );
      }

      setMessages((current) => [
        ...current,
        {
          id: `${Date.now()}-assistant`,
          role: "assistant",
          text:
            result.analysis ||
            "The image was analyzed successfully, but no analysis text was returned.",
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: `${Date.now()}-error`,
          role: "assistant",
          text: `I couldn't analyze that image.\n\n${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleFileSelected = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      analyzeImage(file);
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <span>✦</span>
          </div>

          <div>
            <div className="brand-name">CloudOps AI</div>
            <div className="brand-caption">Enterprise Intelligence</div>
          </div>
        </div>

        <div className="sidebar-label">PLATFORM</div>

        <nav className="navigation">
          {[
            ["Overview", "⌂"],
            ["AI Assistant", "✦"],
            ["Data Intelligence", "▦"],
            ["Research", "⌕"],
            ["Multimodal", "◈"],
            ["Workflows", "◇"],
          ].map(([label, icon]) => (
            <button
              key={label}
              className={`nav-item ${
                activeSection === label ? "active" : ""
              }`}
              onClick={() => setActiveSection(label)}
            >
              <span className="nav-icon">{icon}</span>
              <span>{label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-spacer" />

        <div className="security-card">
          <div className="security-icon">✓</div>

          <div>
            <div className="security-title">Security Active</div>
            <div className="security-text">Tenant isolation enabled</div>
          </div>
        </div>

        <div className="user-card">
          <div className="avatar">RB</div>

          <div className="user-info">
            <div className="user-name">Ronak Bhanushali</div>
            <div className="user-role">Authorized user</div>
          </div>

          <span className="user-status" />
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <div className="breadcrumb">
              CloudOps AI / {activeSection}
            </div>

            <h1>{activeSection}</h1>
          </div>

          <div className="topbar-actions">
            <div className="environment-pill">
              <span className="status-dot" />
              Live Cloud Run
            </div>

            <button className="icon-button" aria-label="Notifications">
              ◌
            </button>

            <button className="profile-button">RB</button>
          </div>
        </header>

        <section className="workspace">
          <div className="hero">
            <div className="hero-badge">
              <span>✦</span>
              AGENTIC AI PLATFORM
            </div>

            <h2>
              Intelligence for your
              <span> cloud operations.</span>
            </h2>

            <p>
              Securely reason across enterprise data, knowledge, documents,
              and workflows with CloudOps AI.
            </p>
          </div>

          <div className="metrics">
            <div className="metric-card">
              <div className="metric-icon purple">✦</div>

              <div>
                <div className="metric-value">4</div>
                <div className="metric-label">Specialist Agents</div>
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-icon blue">⌁</div>

              <div>
                <div className="metric-value">10/10</div>
                <div className="metric-label">Security Tests</div>
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-icon green">✓</div>

              <div>
                <div className="metric-value">RLS</div>
                <div className="metric-label">Tenant Isolation</div>
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-icon orange">☁</div>

              <div>
                <div className="metric-value">Live</div>
                <div className="metric-label">Cloud Run</div>
              </div>
            </div>
          </div>

          <section className="assistant-panel">
            <div className="panel-header">
              <div className="assistant-title">
                <div className="assistant-avatar">✦</div>

                <div>
                  <h3>CloudOps Assistant</h3>

                  <span>
                    <i />
                    {loading ? "Processing request..." : "Ready to assist"}
                  </span>
                </div>
              </div>

              <div className="agent-badge">Root Orchestrator</div>
            </div>

            <div className="messages">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message-row ${message.role}`}
                >
                  {message.role === "assistant" && (
                    <div className="message-avatar">✦</div>
                  )}

                  <div className="message-bubble">
                    {message.role === "assistant" ? renderAssistantText(message.text) : message.text}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message-row assistant">
                  <div className="message-avatar">✦</div>

                  <div className="message-bubble typing">
                    <span />
                    <span />
                    <span />
                  </div>
                </div>
              )}
            </div>

            <div className="suggestions">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => sendMessage(suggestion)}
                  disabled={loading}
                >
                  {suggestion}
                </button>
              ))}
            </div>

            <form className="composer" onSubmit={handleSubmit}>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={handleFileSelected}
                hidden
              />
              <button
                type="button"
                className="composer-tool"
                aria-label="Attach an image"
                onClick={() => fileInputRef.current?.click()}
                disabled={loading}
              >
                +
              </button>

              <input
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="Ask CloudOps AI anything..."
                disabled={loading}
              />

              <button
                type="submit"
                className="send-button"
                disabled={loading || !input.trim()}
              >
                ↑
              </button>
            </form>

            <div className="composer-note">
              AI responses should be verified against authorized enterprise
              data and retrieved sources.
            </div>
          </section>
        </section>
      </main>
    </div>
  );
}

export default App;
