import customtkinter as ctk
import sqlite3

DB_PATH = "C://Users//elijah//Documents//GitHub//monkey_see//Resources//SCDB.db"

def get_table_names():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [name[0] for name in cursor.fetchall()]
    conn.close()
    return tables

def fetch_data(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Seniors")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return columns, rows

def display_table(table_name):
    columns, data = fetch_data(table_name)

    # Clear scrollable frame
    for widget in scrollable_inner.winfo_children():
        widget.destroy()

    # Display column headers
    for col_index, col_name in enumerate(columns):
        header = ctk.CTkLabel(scrollable_inner, text=col_name, width=150)
        header.grid(row=0, column=col_index, padx=5, pady=5, sticky="nsew")

    # Display data rows
    for row_index, row_data in enumerate(data, start=1):
        for col_index, value in enumerate(row_data):
            cell = ctk.CTkLabel(scrollable_inner, text=str(value), width=150)
            cell.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="nsew")

def on_table_select(choice):
    display_table(choice)

# App setup
app = ctk.CTk()
app.title("")
app.geometry("1000x600")

# Dropdown
tables = get_table_names()
if not tables:
    raise Exception("No tables found in the database.")

selected_table = ctk.StringVar(value=tables[0])
dropdown = ctk.CTkOptionMenu(app, values=tables, variable=selected_table, command=on_table_select)
dropdown.pack(pady=10)

# Scrollable frame for table
scrollable_wrapper = ctk.CTkFrame(app)
scrollable_wrapper.pack(pady=10, padx=10, fill="both", expand=True)

scrollable = ctk.CTkScrollableFrame(scrollable_wrapper, orientation="both")
scrollable.pack(fill="both", expand=True)

# Inner frame to hold table content
scrollable_inner = ctk.CTkFrame(scrollable)
scrollable_inner.pack()

# Show default table
display_table(tables[0])

app.mainloop()
