from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
from rich.table import Table
from database import get_all_todos, get_todos_sorted_by_due_date
from time import sleep
import checklist_func
import cutie
import os
import datetime

console = Console()

progress_count = 0
selected_choice = None
sort_by_due_date = False  # Toggle: False = insertion order, True = sort by due date

choices = [
    "Add Tasks",
    "Remove Tasks",
    "Update Tasks",
    "Toggle Sort by Due Date",
    "Close Application"
]

# CATEGORY LIST
category_choices = [
    "Assignment",
    "Quiz",
    "Assessment Task",
    "Notes"
]


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_category():
    print("\nSelect Category:")
    for i, cat in enumerate(category_choices, 1):
        print(f"{i}. {cat}")

    choice = int(input("Enter number: "))

    while choice < 1 or choice > len(category_choices):
        print("Invalid choice. Try again.")
        choice = int(input("Enter number: "))

    return category_choices[choice - 1]


def get_due_date():
    """Prompt user for a due date. Returns ISO date string or None if skipped."""
    print("\nEnter due date (YYYY-MM-DD) or press Enter to skip: ", end="")
    raw = input().strip()

    if not raw:
        return None

    while True:
        try:
            datetime.datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Invalid format. Use YYYY-MM-DD (e.g. 2025-05-20). Try again: ", end="")
            raw = input().strip()
            if not raw:
                return None


def get_due_date_color(due_date_str):
    """Returns a Rich color based on how urgent the due date is."""
    if not due_date_str:
        return 'white'
    try:
        due = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = (due - today).days

        if delta < 0:
            return 'bright_red'    # Overdue
        elif delta <= 2:
            return 'red'           # Due very soon
        elif delta <= 7:
            return 'yellow'        # Due this week
        else:
            return 'green'         # Plenty of time
    except ValueError:
        return 'white'


def show():
    global progress_count
    global selected_choice

    if sort_by_due_date:
        tasks_list = get_todos_sorted_by_due_date()
        sort_label = "[bold cyan]📅 Sorted by Due Date[/bold cyan]"
    else:
        tasks_list = get_all_todos()
        sort_label = "[dim]Sorted by: Insertion Order[/dim]"

    progress_count = 0

    console.print("[bold magenta] To do [/bold magenta]!", "📃", sort_label)

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Type", min_width=18, justify="right")
    table.add_column("Due Date", min_width=12, justify="right")
    table.add_column("Finished", min_width=12, justify="right")

    def get_categ_color(category):
        colors = {
            'Assignment': 'cyan',
            'Quiz': 'yellow',
            'Assessment Task': 'magenta',
            'Notes': 'green'
        }
        return colors.get(category, 'white')

    today = datetime.date.today()

    for idx, task in enumerate(tasks_list, start=1):
        c = get_categ_color(task.category)
        is_done_str = '✅' if task.status == 2 else '❌'

        if task.status == 2:
            progress_count += 1

        # Format due date display
        if task.due_date:
            due_color = get_due_date_color(task.due_date)
            try:
                due = datetime.datetime.strptime(task.due_date, "%Y-%m-%d").date()
                delta = (due - today).days
                if delta < 0:
                    due_display = f"[{due_color}]{task.due_date} (overdue!)[/{due_color}]"
                elif delta == 0:
                    due_display = f"[{due_color}]{task.due_date} (today!)[/{due_color}]"
                elif delta == 1:
                    due_display = f"[{due_color}]{task.due_date} (tomorrow)[/{due_color}]"
                else:
                    due_display = f"[{due_color}]{task.due_date}[/{due_color}]"
            except ValueError:
                due_display = task.due_date
        else:
            due_display = "[dim]—[/dim]"

        table.add_row(str(idx), task.task, f'[{c}]{task.category}[/{c}]', due_display, is_done_str)

    console.print(table)

    total_tasks = len(tasks_list)

    if total_tasks > 0:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%")
        ) as prog:

            task_id = prog.add_task("[green]Completed", total=total_tasks)
            prog.update(task_id, completed=progress_count)

    print("\nWhat would you like to do?")
    selected_choice = choices[cutie.select(choices)]


# =========================
# MAIN LOOP
# =========================

show()

while selected_choice != "Close Application":

    if selected_choice == "Add Tasks":
        num = int(cutie.get_number("How many tasks would you like to add?: "))

        for _ in range(num):
            task = input("Name of task: ")
            category = get_category()
            due_date = get_due_date()
            checklist_func.add(task, category, due_date)
            sleep(1)

    elif selected_choice == "Remove Tasks":
        num = int(cutie.get_number("How many tasks would you like to delete?: "))

        for _ in range(num):
            position = int(cutie.get_number("Enter Task number: "))
            checklist_func.delete(position)
            sleep(1)

    elif selected_choice == "Update Tasks":
        num = int(cutie.get_number("How many tasks would you update?: "))

        # =========================
        # CLEAN UPDATE MENU
        # =========================
        update_choices = [
            "Update Task Name",
            "Update Category",
            "Update Due Date",
            "Mark as Done"
        ]

        for _ in range(num):
            position = int(cutie.get_number("Enter Task number: "))

            action = cutie.select(update_choices)

            # 1. Update Task Name
            if action == 0:
                task = input("New task name: ")
                checklist_func.update(position, task, None)

            # 2. Update Category
            elif action == 1:
                category = get_category()
                checklist_func.update(position, None, category)

            # 3. Update Due Date
            elif action == 2:
                due_date = get_due_date()
                checklist_func.set_due_date(position, due_date)

            # 4. Mark as Done
            elif action == 3:
                checklist_func.complete(position)

            sleep(1)

    elif selected_choice == "Toggle Sort by Due Date":
        sort_by_due_date = not sort_by_due_date
        state = "ON (sorted by due date)" if sort_by_due_date else "OFF (insertion order)"
        console.print(f"[bold green]Sort by due date: {state}[/bold green]")
        sleep(1)

    clear_console()
    show()
