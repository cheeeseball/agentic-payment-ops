"use client";

import { useState, useEffect, useRef } from "react";
import axios from "axios";

type Message = {
    role: "user" | "assistant";
    content: string;
};

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");

    const sendMessage = async () => {
        if (!input.trim()) return;

        const newMessages: Message[] = [
            ...messages,
            { role: "user", content: input }
        ];

        setMessages(newMessages);
        setInput("");

        const res = await axios.post("/api/chat", {
            messages: newMessages
        });

        setMessages([
            ...newMessages,
            { role: "assistant", content: res.data.reply }
        ]);
    };

    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);


    return (
        <div className="flex flex-col h-screen p-6">
            <h1 className="text-2xl font-bold mb-4">GPT-OSS Chatbot</h1>

            <div className="flex-1 overflow-y-auto space-y-3 mb-4">
                {messages.map((msg, i) => (
                    <div
                        key={i}
                        className={`p-3 rounded ${msg.role === "user"
                            ? "self-end"
                            : "self-start"
                            }`}
                    >
                        <b>{msg.role}:</b> {msg.content}
                    </div>
                ))}
                <div ref={bottomRef} />
            </div>

            <div className="flex gap-2">
                <textarea
                    autoFocus
                    className="border p-2 flex-1 rounded resize-none"
                    rows={2}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            sendMessage();
                        }
                    }}
                    placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
                />
                <div ref={bottomRef} />
                <button
                    onClick={sendMessage}
                    className="bg-black text-white px-4 rounded"
                >
                    Send
                </button>
            </div>
        </div>
    );
}
