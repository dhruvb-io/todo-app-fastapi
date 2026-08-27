from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from models import TodoModel
from sqlalchemy.orm import Session
from database import Sessionlocal, engine
from typing import Optional, List

import os

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

TodoModel.metadata.create_all(bind=engine) # Create the table in database

# todos = []

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True # Updated for Pydantic V2 compatibility

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/todos", response_model=List[TodoBase])
@app.get("/todos", response_model=List[TodoResponse]) # Fixed: response model needs to include 'id' via TodoResponse
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoModel).all()
    return todos

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id)
    print(todo.first())
    
    # Added 404 check if todo doesn't exist to prevent server error
    db_todo = todo.first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoModel(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updated_todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_todo.title = updated_todo.title
    db_todo.description = updated_todo.description
    db_todo.completed = updated_todo.completed
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return db_todo