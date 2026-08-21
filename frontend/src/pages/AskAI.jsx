import { useState, useRef, useEffect } from "react";
import { Mic, Send, Sparkles } from "lucide-react";
import { useApp } from "../context/AppContext";
import PageContainer from "../components/layout/PageContainer";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import { chatSuggestions } from "../data/mock";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export default function AskAI() {
  const { t, lang } = useApp();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [thinking, setThinking] = useState(false);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, thinking]);

  async function send(text) {
    const q = (text ?? input).trim();
    if (!q || thinking) return;

    setMessages((m) => [...m, { role: "user", text: q }]);
    setInput("");
    setThinking(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: q,
          language: lang,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "AI assistant request failed.");
      }

      setMessages((m) => [
        ...m,
        {
          role: "ai",
          text: data.reply,
          sources: data.sources ?? [],
        },
      ]);
    } catch (error) {
      setMessages((m) => [
        ...m,
        {
          role: "ai",
          text:
            lang === "hi"
              ? "माफ़ कीजिए, AI सेवा से संपर्क नहीं हो सका। कृपया सुनिश्चित करें कि backend चल रहा है और GEMINI_API_KEY सही है।"
              : `Sorry, I could not reach the AI service. ${error.message}`,
          sources: [],
        },
      ]);
    } finally {
      setThinking(false);
    }
  }

  return (
    <PageContainer className="flex flex-col min-h-[calc(100svh-64px)]">
      <div className="mb-4">
        <h1 className="font-display text-xl font-extrabold text-leaf-900">
          {t("ask_title")}
        </h1>
        <p className="text-ink-600 text-sm mt-1">{t("ask_subtitle")}</p>
      </div>

      {messages.length === 0 ? (
        <Card className="mb-4">
          <p className="text-xs font-semibold text-ink-400 uppercase tracking-wide mb-2.5">
            {t("ask_suggestions")}
          </p>
          <div className="flex flex-col gap-2">
            {chatSuggestions.map((s, i) => (
              <button
                key={i}
                onClick={() => send(lang === "hi" ? s.hi : s.en)}
                className="text-left text-sm text-leaf-800 bg-leaf-100 hover:bg-leaf-100/70 rounded-xl px-3.5 py-2.5 font-medium transition-colors"
              >
                {lang === "hi" ? s.hi : s.en}
              </button>
            ))}
          </div>
        </Card>
      ) : (
        <div className="flex-1 space-y-3 mb-4">
          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex ${
                m.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-snug ${
                  m.role === "user"
                    ? "bg-leaf-800 text-white rounded-br-sm"
                    : "bg-white border border-soil-200 text-ink-900 rounded-bl-sm"
                }`}
              >
                {m.role === "ai" && (
                  <p className="flex items-center gap-1.5 text-leaf-700 text-xs font-bold mb-1.5">
                    <Sparkles size={13} /> {t("common_ai")}
                  </p>
                )}

                <p className="whitespace-pre-wrap">{m.text}</p>

                {m.sources?.length > 0 && (
                  <p className="mt-2 pt-2 border-t border-soil-200 text-[11px] text-ink-400">
                    {m.sources.join(" · ")}
                  </p>
                )}
              </div>
            </div>
          ))}

          {thinking && (
            <div className="flex justify-start">
              <div className="bg-white border border-soil-200 rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1.5">
                <span className="w-2 h-2 rounded-full bg-leaf-400 animate-bounce [animation-delay:-0.3s]" />
                <span className="w-2 h-2 rounded-full bg-leaf-400 animate-bounce [animation-delay:-0.15s]" />
                <span className="w-2 h-2 rounded-full bg-leaf-400 animate-bounce" />
              </div>
            </div>
          )}

          <div ref={endRef} />
        </div>
      )}

      <p className="text-[11px] text-ink-400 text-center mb-2">
        {t("ask_disclaimer")}
      </p>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          send();
        }}
        className="sticky bottom-20 flex items-center gap-2 bg-white border border-soil-200 rounded-2xl p-2 shadow-[0_2px_10px_rgba(47,82,51,0.08)]"
      >
        <button
          type="button"
          aria-label={t("ask_listening")}
          className="grid place-items-center w-11 h-11 rounded-xl bg-soil-100 text-leaf-800 shrink-0"
        >
          <Mic size={19} strokeWidth={2.25} />
        </button>

        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t("ask_placeholder")}
          className="flex-1 bg-transparent outline-none text-sm text-ink-900 placeholder:text-ink-400"
        />

        <Button
          type="submit"
          className="!min-h-[44px] !px-4"
          disabled={!input.trim() || thinking}
        >
          <Send size={18} strokeWidth={2.25} />
        </Button>
      </form>
    </PageContainer>
  );
}
