import { NextRequest, NextResponse } from "next/server";
import axios from "axios";

export async function POST(req: NextRequest) {
  try {
    const { messages } = await req.json();

    const response = await axios.post("http://localhost:11434/api/chat", {
      model: "gpt-oss:20b",
      messages: messages,
      stream: false
    });

    return NextResponse.json({
      reply: response.data.message.content
    });

  } catch (err) {
    return NextResponse.json(
      { error: "Ollama not responding" },
      { status: 500 }
    );
  }
}
