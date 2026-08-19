import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

DB_PATH = "checkpoints.sqlite"

def create_checkpointer() -> SqliteSaver:
    connection = sqlite3.connect(DB_PATH,check_same_thread=False)
    return SqliteSaver(connection)