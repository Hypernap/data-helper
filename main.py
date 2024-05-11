import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import os

def clean_data(df, key_column):
    cleaned_df = df.dropna(subset=[key_column])
    return cleaned_df

def process_file(file_path, key_column):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.csv':
        df = pd.read_csv(file_path)
    elif file_extension.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        print("Unsupported file format.")
        return None

    cleaned_df = clean_data(df, key_column)
    return cleaned_df

def select_key_column(filename):
    root = tk.Tk()
    root.title("Select Key Column")

    def submit():
        selected_column = listbox.get(tk.ACTIVE)
        cleaned_df = process_file(file_path, selected_column)
        if cleaned_df is not None:
            root.destroy()  # Close the select key column window
            show_processed_data(cleaned_df, selected_column)

    file_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.csv':
        df = pd.read_csv(file_path)
    elif file_extension.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path, engine='openpyxl')
    columns = df.columns.tolist()

    listbox = tk.Listbox(root)
    for col in columns:
        listbox.insert(tk.END, col)
    listbox.pack()

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack()

    root.mainloop()

def show_processed_data(dataframe, key_column):
    root = tk.Tk()
    root.title("Processed Data Summary")

    # Create main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Overall Summary Section
    overall_frame = tk.Frame(main_frame, bd=2, relief=tk.GROOVE)
    overall_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    overall_label = tk.Label(overall_frame, text="Overall Summary", font=("Helvetica", 12, "bold"))
    overall_label.pack(pady=5)
    overall_summary_text = tk.Text(overall_frame, height=4, wrap=tk.WORD)
    overall_summary_text.insert(tk.END, dataframe.describe())
    overall_summary_text.config(state=tk.DISABLED)
    overall_summary_text.pack(fill=tk.BOTH, expand=True)
    overall_scrollbar = ttk.Scrollbar(overall_frame, orient="vertical", command=overall_summary_text.yview)
    # overall_summary_text.config(yscrollcommand=overall_scrollbar.set)
    # overall_scrollbar.pack(side="right", fill="y")

    # Individual Column Summaries Section
    column_frame = tk.Frame(main_frame, bd=2, relief=tk.GROOVE)
    column_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    column_label = tk.Label(column_frame, text="Individual Column Summaries", font=("Helvetica", 12, "bold"))
    column_label.pack(pady=5)
    column_summaries = tk.Text(column_frame, height=len(dataframe.columns), wrap=tk.WORD)
    for col in dataframe.columns:
        column_summaries.insert(tk.END, f"\nColumn: {col}\n")
        column_summaries.insert(tk.END, dataframe[col].describe())
        column_summaries.insert(tk.END, "\n----------------------------------------\n")
    column_summaries.config(state=tk.DISABLED)
    column_summaries.pack(fill=tk.BOTH, expand=True)
    column_scrollbar = ttk.Scrollbar(column_frame, orient="vertical", command=column_summaries.yview)
    column_summaries.config(yscrollcommand=column_scrollbar.set)
    column_scrollbar.pack(side="right", fill="y")

    # Treeview Section
    tree_frame = tk.Frame(main_frame, bd=2, relief=tk.GROOVE)
    tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    tree_label = tk.Label(tree_frame, text="Treeview", font=("Helvetica", 12, "bold"))
    tree_label.pack(pady=5)
    tree = ttk.Treeview(tree_frame, show="headings", columns=list(dataframe.columns))
    for col in dataframe.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, minwidth=50, anchor=tk.CENTER)

    for index, row in dataframe.iterrows():
        tree.insert("", tk.END, values=list(row))

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

    # Allow resizing of columns
    for col in dataframe.columns:
        tree.heading(col, text=col, anchor=tk.CENTER, command=lambda c=col: sort_treeview(tree, c, False))
        tree.column(col, width=100, minwidth=50, anchor=tk.CENTER, stretch=True)

    root.mainloop()



def browse_files():
    filename = os.listdir(os.path.join(os.path.dirname(__file__), 'data'))[0]
    select_key_column(filename)

if __name__ == "__main__":
    browse_files()
