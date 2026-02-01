import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

export async function GET() {
  const { rows } = await pool.query("SELECT * FROM banks");
  return NextResponse.json(rows);
}
