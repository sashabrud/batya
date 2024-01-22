from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .debil import SessionLocal, Aneky

api = FastAPI()


class AddJokeRequest(BaseModel):
    text: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_joke_from_memory(db: Session, joke_id: int):
    return db.query(Aneky).filter(Aneky.id == joke_id).first()


def learn_joke(db: Session, request: AddJokeRequest):
    db_joke = Aneky(text=request.text)
    db.add(db_joke)
    db.commit()
    db.refresh(db_joke)
    return db_joke


def fix_joke_in_memory(db: Session, joke_id: int, new_text: str):
    db_joke = db.query(Aneky).filter(Aneky.id == joke_id).first()
    db_joke.text = new_text
    db.commit()
    db.refresh(db_joke)
    return db_joke


def forget_joke(db: Session, joke_id: int):
    db_joke = db.query(Aneky).filter(Aneky.id == joke_id).first()
    db.delete(db_joke)
    db.commit()


def to_html(text):
    return f"<p>{text.replace('\n', '<br>')}</p>"


@api.get("/api/joke/{joke_id}", response_class=HTMLResponse)
def get_joke(joke_id: int, db: Session = Depends(get_db)):
    joke = get_joke_from_memory(db, joke_id)
    if joke is None:
        return HTMLResponse(status_code=404, content="Бать, пей таблетки")
    return to_html(joke.text)


@api.post("/api/joke")
def add_joke(request: AddJokeRequest, db: Session = Depends(get_db)):
    joke = learn_joke(db, request)
    return {"status": "ok", "id": joke.id}


@api.put("/api/joke/{joke_id}/update")
def fix_joke(joke_id: int, request: AddJokeRequest, db: Session = Depends(get_db)):
    joke = fix_joke_in_memory(db, joke_id, request.text)
    return {"status": "ok", "id": joke.id, "text": joke.text}


@api.delete("/api/joke/{joke_id}/delete")
def delete_joke(joke_id: int, db: Session = Depends(get_db)):
    get_joke_from_memory(db, joke_id)
    forget_joke(db, joke_id)
    return {"status": "ok", "text": "Забыл твою шутку у тебя за щекой"}
