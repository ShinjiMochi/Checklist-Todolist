import typer

def add(task: str, category: str):
    typer.echo(f"Adding {task, category}")

def delete(position: int):
    typer.echo(f"Deleting {position}")

def update(position: int, task: str = None, category: str = None):
    typer.echo(f"Updating status of task {position}")