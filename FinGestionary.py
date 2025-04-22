import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# === Paramètres de style ===
BG_COLOR = "#FFE5B4"
BTN_COLOR = "#FF8C42"
TEXT_COLOR = "#333"
FONT = ("Helvetica", 12)

# === Initialisation base de données ===
conn = sqlite3.connect("fingestionary.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    category TEXT,
    description TEXT,
    date TEXT)""")
conn.commit()


# === Connexion / Inscription ===
def register():
    username = username_entry.get()
    password = password_entry.get()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Inscription", "Compte créé avec succès.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erreur", "Nom d'utilisateur déjà utilisé.")

def login():
    username = username_entry.get()
    password = password_entry.get()
    cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    if user:
        login_window.destroy()
        open_main_app(user[0])
    else:
        messagebox.showerror("Erreur", "Identifiants incorrects.")


# === Application principale ===
def open_main_app(user_id):
    root = tk.Tk()
    root.title("FinGestionary")
    root.geometry("800x600")
    root.configure(bg=BG_COLOR)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill="both")

    style = ttk.Style()
    style.configure("TNotebook.Tab", font=("Helvetica", 11, "bold"))

    # === Onglet 1 : Tableau de bord ===
    dashboard_frame = tk.Frame(notebook, bg=BG_COLOR)
    notebook.add(dashboard_frame, text="Tableau de bord")

    tree = ttk.Treeview(dashboard_frame, columns=("Montant", "Catégorie", "Description", "Date"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(expand=1, fill="both", pady=10, padx=10)

    def load_expenses():
        for i in tree.get_children():
            tree.delete(i)
        cur.execute("SELECT amount, category, description, date FROM expenses WHERE user_id=?", (user_id,))
        for row in cur.fetchall():
            tree.insert("", "end", values=row)

    load_expenses()

    # === Onglet 2 : Ajouter une dépense ===
    add_frame = tk.Frame(notebook, bg=BG_COLOR)
    notebook.add(add_frame, text="Ajouter une dépense")

    tk.Label(add_frame, text="Montant (€)", bg=BG_COLOR).pack(pady=5)
    amount_entry = tk.Entry(add_frame)
    amount_entry.pack()

    tk.Label(add_frame, text="Catégorie", bg=BG_COLOR).pack(pady=5)
    category_entry = tk.Entry(add_frame)
    category_entry.pack()

    tk.Label(add_frame, text="Description", bg=BG_COLOR).pack(pady=5)
    desc_entry = tk.Entry(add_frame)
    desc_entry.pack()

    def add_expense():
        try:
            amount = float(amount_entry.get())
            category = category_entry.get()
            description = desc_entry.get()
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            cur.execute("INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
                        (user_id, amount, category, description, date))
            conn.commit()
            messagebox.showinfo("Succès", "Dépense ajoutée.")
            amount_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
            load_expenses()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")

    tk.Button(add_frame, text="Ajouter", bg=BTN_COLOR, fg="white", command=add_expense).pack(pady=10)

    # === Onglet 3 : Statistiques (à venir) ===
    stats_frame = tk.Frame(notebook, bg=BG_COLOR)
    notebook.add(stats_frame, text="Statistiques")
    tk.Label(stats_frame, text="À venir...", bg=BG_COLOR).pack(pady=20)

    # === Onglet 4 : Export PDF (à venir) ===
    export_frame = tk.Frame(notebook, bg=BG_COLOR)
    notebook.add(export_frame, text="Exporter PDF")
    tk.Label(export_frame, text="Fonction à venir...", bg=BG_COLOR).pack(pady=20)

    root.mainloop()


# === Interface de connexion ===
login_window = tk.Tk()
login_window.title("Connexion - FinGestionary")
login_window.geometry("400x350")
login_window.configure(bg=BG_COLOR)

tk.Label(login_window, text="FinGestionary", font=("Helvetica", 24, "bold"), fg=BTN_COLOR, bg=BG_COLOR).pack(pady=20)

tk.Label(login_window, text="Nom d'utilisateur", bg=BG_COLOR).pack()
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(login_window, text="Mot de passe", bg=BG_COLOR).pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

tk.Button(login_window, text="Se connecter", bg=BTN_COLOR, fg="white", command=login).pack(pady=10)
tk.Button(login_window, text="S'inscrire", bg="#aaa", fg="white", command=register).pack()

login_window.mainloop()
