### check requirements.txt for the needed modules ###

from rich.progress import Progress, BarColumn, TextColumn ## progress bar module
from rich.console import Console ## Displaying of table 
from rich.table import Table ## Creation of table
from database import get_all_todos ## task import
from time import sleep
import checklist_func
import cutie ## Selection module
import sys 

console = Console()
progress = Progress()
progress_count = 0
progress_previous = 0

## Choices the cutie.select function will call
choices = [
    "Add Tasks",
    "Remove Tasks",
    "Update Tasks",
    "Complete Tasks",
    "Close Application"
]  

def show():
    tasks = get_all_todos()
    global progress_count
    global progress_previous

    ## Table creation ##
    console.print("[bold magenta] To do [/bold magenta]!", "📃")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6) ## Tasks number (first column)
    table.add_column("Todo", min_width=20) ## Task description
    table.add_column("Category", min_width=12, justify="right") ## Self explanitory
    table.add_column("Finished",  min_width=12, justify="right") ## Tasks status

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
    
    ## Progress bar (empty because still trying to understand)

    progress.start()
    try:
        total_progress_done = progress.add_task("[green]Total Completed", total=table.row_count)
        if progress_previous > progress_count:
            progress.update(total_progress_done, completed=progress_count)
            progress_previous = progress_count
    finally:
        progress.stop()
    
## Selection screen ##

show() ## Calls the show function to print the table

print("What would you like to do?")
selected_choice = choices[cutie.select(choices)] ## selection function

if selected_choice == "Add Tasks":
    num_tasks_toadd = cutie.get_number("How many tasks would you like to add?: ")
    task = cutie.secure_input("Name of task: ")
    print("Category list:\n -Excercise \n -Study \n -Learn")
    category = cutie.secure_input("Category of task? (CASE SENSITIVE): ")
    for i in range(num_tasks_toadd):
        checklist_func.add(task, category)
        sleep(0.2)
    
elif selected_choice == "Remove Tasks":
    num_tasks_todel = cutie.get_number("How many tasks would you like to delete?: ")
    for i in range(num_tasks_todel):
        position = cutie.get_number("Enter Task number: ")
        checklist_func.delete(position)
        sleep(0.2)

elif selected_choice == "Update Tasks":
    num_tasks_toupd = cutie.get_number("How many tasks would you like to update?: ")
    for i in range(num_tasks_toupd):
        position = cutie.get_number("Enter Task number: ")
        checklist_func.update(position)
        sleep(0.2)
        
elif selected_choice == "Mark tasks as Complete":
    num_tasks_tomark = cutie.get_number("How many tasks would you to mark completed?: ")
    for i in range(num_tasks_tomark):
        position = cutie.get_number("Enter Task number: ")
        checklist_func.complete(position)
        sleep(0.2)

elif selected_choice == "Close":
    sys.exit()