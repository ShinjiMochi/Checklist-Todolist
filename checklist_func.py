import typer
from model import Todo
from database import delete_todo, insert_todo, complete_todo, update_todo, update_due_date

def add(task: str, category: str, due_date: str = None): ## adds Tasks
    typer.echo(f"Adding {task, category}")
    todo = Todo(task, category, due_date=due_date)
    insert_todo(todo)

def delete(position: int): ## Deletes Tasks
    typer.echo(f"Deleting {position}")
    #indicies in UI begin at 1, but in database it begins at 0
    delete_todo(position-1)

def update(position: int, task: str = None, category: str = None): ## Updates tasks description and category
    typer.echo(f"Updating status of task {position}")
    update_todo(position-1, task, category)

def set_due_date(position: int, due_date: str): ## Sets or updates a task's due date
    typer.echo(f"Setting due date for task {position} to {due_date}")
    update_due_date(position-1, due_date)

def complete(position: int): ## Marks tasks complete
    typer.echo(f"Marking complete {position}")
    #indicies in UI begin at 1, but in database it begins at 0
    complete_todo(position-1)
