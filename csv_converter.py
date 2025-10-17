import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

def open_csv():
    # Ask user to pick CSV file
    csv_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not csv_path:
        return

    try:
        data = pd.read_csv(csv_path)

        # Normalize column names (lowercase and strip spaces)
        data.columns = [col.strip().lower() for col in data.columns]

        # ✅ Expect 'category' and 'message' columns (case-insensitive)
        if not {'category', 'message'}.issubset(data.columns):
            messagebox.showerror(
                "Error",
                f"CSV must have 'Category' and 'Message' columns.\n\nFound: {list(data.columns)}"
            )
            return

        # Display CSV content
        show_csv_data(data)

        # Extract messages
        extract_messages(data, csv_path)

    except Exception as e:
        messagebox.showerror("Error", f"Could not process CSV:\n{e}")

def show_csv_data(data):
    """Display CSV data in a table"""
    for i in tree.get_children():
        tree.delete(i)
    tree["columns"] = list(data.columns)

    for col in data.columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=350)

    for _, row in data.iterrows():
        tree.insert("", "end", values=list(row))

def extract_messages(data, csv_path):
    """Create category folders and save messages"""
    base_folder = os.path.join(os.path.dirname(csv_path), "Extracted_Messages")
    os.makedirs(base_folder, exist_ok=True)

    count = 0
    for _, row in data.iterrows():
        category = str(row["category"]).strip()
        message = str(row["message"]).strip()

        category_folder = os.path.join(base_folder, category)
        os.makedirs(category_folder, exist_ok=True)

        filename = f"message_{count + 1}.txt"
        filepath = os.path.join(category_folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(message)

        count += 1

    messagebox.showinfo(
        "Extraction Complete",
        f"✅ {count} messages extracted!\n📁 Saved in: {base_folder}"
    )

# --- GUI setup ---
root = tk.Tk()
root.title("CSV Message Extractor")
root.geometry("800x500")
root.resizable(False, False)

title_label = ttk.Label(root, text="📄 CSV Message Extractor", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

open_button = ttk.Button(root, text="Select CSV File", command=open_csv)
open_button.pack(pady=10)

tree = ttk.Treeview(root)
tree.pack(expand=True, fill="both", padx=10, pady=10)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

root.mainloop()
