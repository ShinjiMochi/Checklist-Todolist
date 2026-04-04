### check requirements.txt for the needed modules ###

from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
from rich.table import Table, Column
from time import sleep
import checklist_func
import cutie
import sys

console = Console()

choices = [
    "Add Tasks",
    "Remove Tasks",
    "Update Tasks",
    "Close Application"
]

def show():
    tasks = [("To do 1", "Study"), ("To do 2", "Excercise")]

    ## Table creation ##
    console.print("[bold magenta] To do [/bold magenta]!", "📃")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Finished",  min_width=12, justify="right")

    def get_categ_color(category):
        colors = {'Learn' : 'cyan', 'Excercise' : 'orange', 'Study' : 'green'}
        if category in colors:
            return colors[category]
        return 'white'

    for idx, tasks in enumerate(tasks, start=1):
        c = get_categ_color(tasks[1])
        is_done_str = '✅' if True == 2 else '❌'
        table.add_row(str(idx), tasks[0], f'[{c}]{tasks[1]}[/{c}]', is_done_str)

    console.print(table) ## displays the table
    
    ## Progress bar (empty because still trying to understand)



## Selection screen ##

show()

print("What would you like to do?")
selected_choice = choices[cutie.select(choices)]

if selected_choice == "Add":
    no_tasks_toadd = input("How many tasks would you like to add?: ")
    for i in range(no_tasks_toadd):
        checklist_func.add
elif selected_choice == "Remove":
    checklist_func.delete
elif selected_choice == "Update":
    checklist_func.update
elif selected_choice == "Close":

    sys.exit()