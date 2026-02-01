import { spawn } from "child_process";
import path from "path";

export async function POST() {
  const scriptPath = path.join(process.cwd(), "system", "system.py");
  console.log("RUNNING:", scriptPath);

  spawn("python", [scriptPath], {
    stdio: "inherit",
  });

  return new Response("agent started");
}
