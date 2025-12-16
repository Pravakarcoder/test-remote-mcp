from fastmcp import FastMCP
import asyncpg
import os

DATABASE_URL =  "postgresql://postgres:pGnbmLDFDBUdE1Zz@db.ioadgyfuafwoonxtujsd.supabase.co:5432/postgres"

mcp = FastMCP("Expense Tracker MCP")

pool: asyncpg.Pool = None


async def init_db():
    global pool
    pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=5,
        max_size=20  # handles concurrency
    )

    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            date TEXT NOT NULL,
            amount NUMERIC NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
        );
        """)


@mcp.on_startup()
async def startup():
    await init_db()


@mcp.tool()
async def add_expense(
    user_id: str,
    date: str,
    amount: float,
    category: str,
    subcategory: str = "",
    note: str = ""
):
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO expenses (user_id, date, amount, category, subcategory, note)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
        """, user_id, date, amount, category, subcategory, note)

    return {
        "status": "success",
        "expense_id": row["id"]
    }


@mcp.tool()
async def list_expenses(user_id: str):
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT * FROM expenses
            WHERE user_id = $1
            ORDER BY date DESC
        """, user_id)

    return [dict(row) for row in rows]


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )
