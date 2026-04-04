import typer
from model import Todo
from database import delete_todo, insert_todo, complete_todo, update_todo

def add(task: str, category: str): ## adds Tasks
    typer.echo(f"Adding {task, category}")
    todo = Todo(task, category)
    insert_todo(todo)

def delete(position: int): ## Deletes Tasks
    typer.echo(f"Deleting {position}")
    #indicies in UI begin at 1, but in database it begins at 0
    delete_todo(position-1)

def update(position: int, task: str = None, category: str = None): ## Updates tasks description and category
    typer.echo(f"Updating status of task {position}")
    update_todo(position-1, task, category)

def complete(position: int): ## Marks tasks complete
    typer.echo(f"Marking complete {position}")
    #indicies in UI begin at 1, but in database it begins at 0
    complete_todo(position-1)