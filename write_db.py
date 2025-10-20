import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# --- Database setup ---
def init_db():
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            "user id" TEXT NOT NULL,
            "battery level" TEXT NOT NULL,
            "user status" TEXT NOT NULL,
            "timestamp" TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- Button Callback ---
def save_entry():
    user_id_text = userId_box.get()
    user_batt_text = userBatt_box.get()
    user_state_text = userStat_box.get()
    if not user_id_text.strip():
        messagebox.showwarning("Empty Entry", "Please enter some text")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # create a DB with user id
    db_name = f"{user_id_text}.db"


    connAllUser = sqlite3.connect("entries.db")
    cursorAllUser = connAllUser.cursor()

    connUser = sqlite3.connect(db_name)
    cursorUser = connUser.cursor()

    # Ensure table exists in user-specific DB
    cursorUser.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            "battery level" TEXT NOT NULL,
            "user status" TEXT NOT NULL,
            "timestamp" TEXT NOT NULL
        )
    """)

    
    # Delete existing rows with the same text
    cursorAllUser.execute("""DELETE FROM logs WHERE "user id" = ?""", (user_id_text,))

    # Insert new entry for all user DB
    cursorAllUser.execute("""
        INSERT INTO logs (
            "user id",
            "battery level",
            "user status",
            timestamp) VALUES (?, ?, ?, ?)""",
            (user_id_text, user_batt_text, user_state_text, timestamp))
    connAllUser.commit()
    connAllUser.close()

    # Insert new entry for all current user
    cursorUser.execute("""
        INSERT INTO logs (
            "battery level",
            "user status",
            timestamp) VALUES (?, ?, ?)""",
            (user_batt_text, user_state_text, timestamp))
    connUser.commit()
    connUser.close()

    messagebox.showinfo("Saved", f"Entry saved at {timestamp}")
    userId_box.delete(0, tk.END)
    userBatt_box.delete(0, tk.END)
    userStat_box.delete(0, tk.END)

#  --- GUI Setup ---
init_db()
root = tk.Tk()
root.title("Text Logger")
root.geometry("400x300")

# --- User ID ---
frame_user = tk.Frame(root)
frame_user.pack(pady=5)
tk.Label(frame_user, text="User ID:", width=12, anchor='w').pack(side=tk.LEFT)
userId_box = tk.Entry(frame_user, width=30)
userId_box.pack(side=tk.LEFT)

# --- Battery Level ---
frame_batt = tk.Frame(root)
frame_batt.pack(pady=5)
tk.Label(frame_batt, text="Battery Level:", width=12, anchor='w').pack(side=tk.LEFT)
userBatt_box = tk.Entry(frame_batt, width=30)
userBatt_box.pack(side=tk.LEFT)

# --- User Status ---
frame_stat = tk.Frame(root)
frame_stat.pack(pady=5)
tk.Label(frame_stat, text="User Status:", width=12, anchor='w').pack(side=tk.LEFT)
userStat_box = tk.Entry(frame_stat, width=30)
userStat_box.pack(side=tk.LEFT)

# --- Save Button ---
save_button = tk.Button(root, text="Save to DB", command=save_entry)
save_button.pack(pady=10)

root.mainloop()

# adding 1st command in master branch
