from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP("Expense Tracker MCP")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )"""
        )
        c.commit()  # Added explicit commit

init_db()

@mcp.tool()
def add_expense( date: str, amount: float, category: str, subcategory: str = "", note: str = ""):
    """Add a new expense to the tracker"""
    with sqlite3.connect(DB_PATH) as c:
        cursor = c.execute(
            "INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note),
        )
        c.commit()
        return {"status": "success", "message": "Expense added successfully.", "id": cursor.lastrowid}

@mcp.tool()
def list_expenses():
    """List all expenses in the tracker"""
    with sqlite3.connect(DB_PATH) as c:
        c.row_factory = sqlite3.Row
        cursor = c.execute("SELECT * FROM expenses ORDER BY date DESC")
        return [dict(row) for row in cursor.fetchall()]

 

# Start the server
if __name__ == "__main__":
    mcp.run(transport = "http", host = "0.0.0.0", port = 8000)
    

