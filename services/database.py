"""Persistência e consultas de produtos no SQLite."""
import sqlite3
from config import DB_PATH

INITIAL_PRODUCTS = [
    ("Notebook", "Informática", 3500.0, 8),
    ("Mouse", "Periféricos", 80.0, 25),
    ("Teclado", "Periféricos", 150.0, 12),
    ("Monitor", "Informática", 950.0, 5),
]


def initialize_database():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )""")
        if con.execute("SELECT COUNT(*) FROM produtos").fetchone()[0] == 0:
            con.executemany(
                "INSERT INTO produtos (nome, categoria, preco, estoque) VALUES (?, ?, ?, ?)",
                INITIAL_PRODUCTS,
            )


def list_categories():
    with sqlite3.connect(DB_PATH) as con:
        return [r[0] for r in con.execute("SELECT DISTINCT categoria FROM produtos ORDER BY categoria")]


def query_products(category="Todas"):
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        if category == "Todas":
            rows = con.execute("SELECT nome, categoria, preco, estoque FROM produtos ORDER BY nome").fetchall()
        else:
            rows = con.execute(
                "SELECT nome, categoria, preco, estoque FROM produtos WHERE categoria = ? ORDER BY nome",
                (category,),
            ).fetchall()
    return [dict(r) for r in rows]
