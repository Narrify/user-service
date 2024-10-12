from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

import database.models as models
from database.database import engine
from database.database import SessionLocal
from database.models import User


#crea las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)



app=FastAPI()

def crear_usuario(user):
    db=SessionLocal()
    db.add(user)
    db.commit()





class UserPyda(BaseModel):
    username: str
    password: str

@app.post('/user')
async def create_user(user: UserPyda):
    crear_usuario(user)
    return "creaste un nuevo usuario"
@app.get('/user/{username}')
async def read_user(username: str):
    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()
    print(f"el usuario del parametro es: {username}")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)


