### check requirements.txt for the needed modules ###

from rich.progress import Progress, BarColumn, TextColumn ## progress bar module
from rich.console import Console ## Displaying of table 
from rich.table import Table ## Creation of table
from database import get_all_todos ## task import
from time import sleep
import checklist_func
import cutie ## Selection module
import sys
import os

console = Console()
progress = Progress()
progress_count = 0
progress_previous = 0
selected_choice = None
progress_bar_created = False

## Choices the cutie.select function will call
choices = [
    "Add Tasks",
    "Remove Tasks",
    "Update Tasks",
    "Mark tasks as Complete",
    "Close Application"
] 

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show():
    tasks = get_all_todos()
    global progress_count
    global progress_previous
    global selected_choice
    global table
    global progress_bar_created

    ## Table creation ##
    console.print("[bold magenta] To do [/bold magenta]!", "📃")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6) ## Tasks number (first column)
    table.add_column("Todo", min_width=20) ## Task description
    table.add_column("Category", min_width=12, justify="right") ## Self explanitory
    table.add_column("Finished",  min_width=12, justify="right") ## Tasks status

    if progress_bar_created == False:
        total_progress_done = progress.add_task("[green]Total Completed", total=table.row_count)
        progress_bar_created = True
    
    ## Category colors
    def get_categ_color(category):
        colors = {'Learn' : 'cyan', 'Excercise' : 'orange', 'Study' : 'green'} ## dictionary for category colors
        if category in colors:
            return colors[category]
        return 'white'

    ## 
    for idx, tasks in enumerate(tasks, start=1):
        c = get_categ_color(tasks.category)
        is_done_str = '✅' if tasks.status == 2 else '❌'
        if is_done_str == '✅':
            progress_count =+ 1
        table.add_row(str(idx), tasks.task, f'[{c}]{tasks.category}[/{c}]', is_done_str)

    console.print(table) ## displays the table
    
    ## Progress bar (still trying to understand)

    progress.start()
    if progress_previous > progress_count:
        progress.update(total_progress_done, completed=progress_count)
        progress_previous = progress_count
    progress.stop()
    
    print("What would you like to do?")
    selected_choice = choices[cutie.select(choices)]
    
## Selection screen ##

show() ## Calls the show function to print the table

while selected_choice  != 'Close':
    if selected_choice == "Add Tasks":
        num_tasks_toadd = int(cutie.get_number("How many tasks would you like to add?: "))
        for i in range(num_tasks_toadd):
            task = str(input("Name of task: "))
            print("Category list:\n Excercise \n Study \n Learn")
            category = str(input("Category of task? (CASE SENSITIVE): "))
            checklist_func.add(task, category)
            sleep(1)
        clear_console()
        show()
        
    elif selected_choice == "Remove Tasks":
        num_tasks_todel = int(cutie.get_number("How many tasks would you like to delete?: "))
        for i in range(num_tasks_todel):
            position = int(cutie.get_number("Enter Task number: "))
            checklist_func.delete(position)
            sleep(1)
        clear_console()
        show()

    elif selected_choice == "Update Tasks":
        num_tasks_toupd = cutie.get_number("How many tasks would you to mark completed?: ")
        for i in range(num_tasks_toupd):
            position = int(cutie.get_number("Which would you like to update?: "))
            task = str(input("Name of task: "))
            print("Category list:\n Excercise \n Study \n Learn")
            category = str(input("Category of task? (CASE SENSITIVE): "))
            position = int(cutie.get_number("Enter Task number: "))
            checklist_func.update(position, task, category)
            sleep(1)
        clear_console()
        show()
            
    elif selected_choice == "Mark tasks as Complete":
        num_tasks_tomark = int(cutie.get_number("How many tasks would you to mark completed?: "))
        for i in range(num_tasks_tomark):
            position = int(cutie.get_number("Enter Task number: "))
            checklist_func.complete(position)
            sleep(1)
        clear_console()
        show()