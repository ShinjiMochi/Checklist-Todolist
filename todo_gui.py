import tkinter as tk
from tkinter import ttk, messagebox
import checklist_func
from database import get_all_todos, get_todos_sorted_by_due_date
import datetime

# =========================
# GREEN THEME COLORS
# =========================
BG = "#305480"
CARD = "#9bc1d9"
ACCENT = "#e1f6f7"
ACCENT_SOFT = "#e5f6f7"
TEXT = "#BFD4DB"
TEXT2 = "#305480"
MUTED = "#88AED0"
BAR_EMPTY = "#555555"

# =========================
# MAIN APP
# =========================
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Manager")
        self.root.geometry("900x700")
        self.root.configure(bg=BG)

        self.sort_by_due = False

        self.setup_ui()
        self.load_tasks()

    # =========================
    # UI SETUP
    # =========================
    def setup_ui(self):
        title = tk.Label(
            self.root,
            text="📋 TaskMan",
            font=("Helvetica", 22, "bold"),
            bg=BG,
            fg=ACCENT
        )
        title.pack(pady=15)

        # STYLE
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background=CARD,
                        foreground=TEXT,
                        fieldbackground=CARD,
                        rowheight=35,
                        font=("Helvetica", 11, "bold"))

        style.configure("Treeview.Heading",
                        font=("Helvetica", 12, "bold"),
                        background=ACCENT_SOFT,
                        foreground="black")

        style.map("Treeview",
                  background=[("selected", ACCENT)])

        # ✅ PROGRESS BAR STYLES (NEW FIX)
        style.configure(
            "Green.Horizontal.TProgressbar",
            troughcolor=CARD,
            background=ACCENT,
            bordercolor=CARD,
            lightcolor=ACCENT,
            darkcolor=ACCENT
        )

        style.configure(
            "Gray.Horizontal.TProgressbar",
            troughcolor=CARD,
            background=BAR_EMPTY,
            bordercolor=CARD
        )

        # TABLE FRAME
        table_frame = tk.Frame(self.root, bg=CARD)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Task", "Category", "Due Date", "Days Left", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # BUTTONS
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=5)

        def btn(text, cmd, col):
            tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                bg=ACCENT,
                fg="black",
                activebackground=ACCENT_SOFT,
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                padx=10,
                pady=5
            ).grid(row=0, column=col, padx=8, pady=8)

        btn("Add Task", self.add_task, 0)
        btn("Delete Task", self.delete_task, 1)
        btn("Update Task", self.update_task, 2)
        btn("Mark Done", self.mark_done, 3)
        btn("Toggle Sort", self.toggle_sort, 4)

        # PROGRESS
        self.progress_label = tk.Label(
            self.root,
            text="Progress: 0%",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 11, "bold")
        )
        self.progress_label.pack()

        # ✅ DEFAULT STYLE = GRAY
        self.progress = ttk.Progressbar(
            self.root,
            length=500,
            style="Gray.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=10)

    # =========================
    # DAYS LEFT LOGIC
    # =========================
    def get_days_left(self, due):
        if not due:
            return "-", "white"

        try:
            due_date = datetime.datetime.strptime(due, "%Y-%m-%d").date()
            today = datetime.date.today()
            delta = (due_date - today).days

            if delta < 0:
                return f"{abs(delta)} day(s) overdue", "#F93E34"
            elif delta == 0:
                return "Due today!", "#FFB64A"
            elif delta <= 2:
                return f"{delta} day(s)", "#FFB64A"
            elif delta <= 7:
                return f"{delta} day(s)", "#FFF27C"
            else:
                return f"{delta} day(s)", "#AEFF9F"
        except:
            return "-", "white"

    # =========================
    # LOAD TASKS
    # =========================
    def load_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tasks = get_todos_sorted_by_due_date() if self.sort_by_due else get_all_todos()

        completed = 0

        for task in tasks:
            status = "✅" if task.status == 2 else "❌"

            if task.status == 2:
                completed += 1

            days_left, color = self.get_days_left(task.due_date)

            row_id = self.tree.insert("", "end", values=(
                task.task,
                task.category,
                task.due_date if task.due_date else "-",
                days_left,
                status
            ))

            self.tree.tag_configure(color, foreground=color)
            self.tree.item(row_id, tags=(color,))

        total = len(tasks)

        if total > 0:
            percent = (completed / total) * 100
        else:
            percent = 0

        self.progress["value"] = percent
        self.progress_label.config(text=f"Progress: {int(percent)}%")

        # ✅ SWITCH BAR COLOR BASED ON PROGRESS
        if percent > 0:
            self.progress.config(style="Green.Horizontal.TProgressbar")
        else:
            self.progress.config(style="Gray.Horizontal.TProgressbar")

    # =========================
    # ACTIONS
    # =========================
    def add_task(self):
        self.popup("Add Task")

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("Warning", "Select a task")

        index = self.tree.index(selected[0]) + 1
        checklist_func.delete(index)
        self.load_tasks()

    def update_task(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("Warning", "Select a task")

        index = self.tree.index(selected[0]) + 1
        self.popup("Update Task", index)

    def mark_done(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("Warning", "Select a task")

        index = self.tree.index(selected[0]) + 1
        checklist_func.complete(index)
        self.load_tasks()

    def toggle_sort(self):
        self.sort_by_due = not self.sort_by_due
        self.load_tasks()

    # =========================
    # POPUP FORM
    # =========================
    def popup(self, title, index=None):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("350x320")
        win.configure(bg=CARD)

        tk.Label(win, text="Task", bg=CARD, fg=TEXT2).pack(pady=5)
        task_entry = tk.Entry(win)
        task_entry.pack()

        tk.Label(win, text="Category", bg=CARD, fg=TEXT2).pack(pady=5)
        category = ttk.Combobox(win, values=[
            "Assignment", "Quiz", "Assessment Task", "Notes"
        ])
        category.pack()

        tk.Label(win, text="Due Date (YYYY-MM-DD)", bg=CARD, fg=TEXT2).pack(pady=5)
        due_entry = tk.Entry(win)
        due_entry.pack()

        def submit():
            task = task_entry.get()
            cat = category.get()
            due = due_entry.get()

            if index:
                checklist_func.update(index, task or None, cat or None)
                if due:
                    checklist_func.set_due_date(index, due)
            else:
                checklist_func.add(task, cat, due if due else None)

            win.destroy()
            self.load_tasks()

        tk.Button(win, text="Submit", bg=ACCENT, fg="black",
                  command=submit).pack(pady=15)


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()