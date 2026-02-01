import { NextResponse } from "next/server";
import { Pool } from "pg";

const pool = new Pool({
  host: "localhost",
  database: "FirmPay",
  user: "postgres",
  password: "imaad@376",
  port: 5432,
});

export async function GET() {
  try {
    const result = await pool.query(
      "SELECT * FROM drafts ORDER BY created_at DESC"
    );

    return NextResponse.json(result.rows);
  } catch (error) {
    console.error("Error fetching drafts:", error);
    return NextResponse.json(
      { error: "Failed to fetch drafts" },
      { status: 500 }
    );
  }
}
