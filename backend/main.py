from fastapi import FastAPI, Depends, HTTPException , Query
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import auth
from jose import JWTError, jwt
from fastapi import Security
from enum import Enum

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=database.engine)

class SortField(str, Enum):
    created_at = "created_at"
    completed = "completed"
    due_date = "due_date"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid auth")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return db.query(models.User).filter(models.User.username == username).first()


@app.post("/todos/", response_model=schemas.TodoOut)
def create_todo(todo: schemas.TodoCreate,
                db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    return crud.create_todo(db, todo, user)

@app.get("/todos/", response_model=list[schemas.TodoOut])
def read_todos(
    completed: Optional[bool] = Query(None),
    sort_by: SortField = Query(SortField.created_at),
    sort_order: SortOrder = Query(SortOrder.desc),
    db: Session = Depends(get_db)
):
    query = db.query(models.Todo)

    if completed is not None:
        query = query.filter(models.Todo.completed == completed)

    # Get the actual SQLAlchemy column from the model
    sort_column = getattr(models.Todo, sort_by.value)

    # Apply sorting
    if sort_order == SortOrder.asc:
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.all()


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)
    return {"detail": "Deleted"}

@app.put("/todos/{todo_id}", response_model=schemas.TodoOut)
def update_todo(todo_id: int, data: schemas.TodoUpdate, db: Session = Depends(get_db)):
    updated = crud.update_todo(db, todo_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="To-Do not found")
    return updated

from datetime import datetime

@app.get("/todos/overdue", response_model=list[schemas.TodoOut])
def get_overdue_todos(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    return db.query(models.Todo).filter(
        models.Todo.due_date < now,
        models.Todo.completed == False
    ).all()


@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user or not auth.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/todos/stats", response_model=schemas.TodoStats)
def get_todo_stats(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    now = datetime.utcnow()

    todos = db.query(models.Todo).filter(models.Todo.owner_id == user.id).all()

    total = len(todos)
    completed = sum(todo.completed for todo in todos)
    pending = total - completed
    overdue = sum(1 for todo in todos if todo.due_date and todo.due_date < now and not todo.completed)

    return schemas.TodoStats(
        total=total,
        completed=completed,
        pending=pending,
        overdue=overdue
    )