from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import shutil
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

MAIN_PATH = os.path.abspath(os.getcwd())
UPLOAD_FOLDER = MAIN_PATH + '/users/images'

# se o diretorio do usuario nao existe, cria um novo diretorio
def user_directory(path_temp, user_id):
    user_path = path_temp + '/' + str(user_id)

    if os.path.exists(user_path):
        return user_path
    else: 
        os.makedirs(user_path)
    return user_path 

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Lista todas as imagens cadastradas
@app.get("/images/", response_model=List[schemas.Image])
def read_images(db: Session = Depends(get_db)):
    images = crud.get_images(db)
    return images

# Listas as imagens de um usuario
@app.get("/users/{user_id}/images/", response_model=List[schemas.Image])
def read_images_from_user(user_id: int, db: Session = Depends(get_db)):
    user_images = crud.get_images_from_user(db, user_id)
    return user_images

@app.get("/users/{user_id}/images/{image_id}", response_model=List[schemas.Image])
def read_image_from_user(user_id: int, image_id:int, db: Session = Depends(get_db)):
    user_image = crud.get_image_from_user(db, user_id, image_id)
    return user_image

# Faz o upload da imagem
@app.post("/users/{user_id}/images/{name_file}")
async def create_upload_file(user_id: int, name_file:str, db: Session = Depends(get_db), file: UploadFile = File(...)):
    print(f"Uploading {name_file} para o usuario {user_id} ")
    path_to_save_image = user_directory(UPLOAD_FOLDER, user_id)
    print(f"Arquivo {name_file} copiado para {path_to_save_image}/{file.filename}")
    new_path = path_to_save_image + '/' + file.filename
    with open(f'{new_path}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    print("Upload complete")
    image = schemas.ImageCreate(name=name_file, path=path_to_save_image)
    crud.create_user_image(db=db, image=image, user_id=user_id) #cadastra uma imagem do usuario
    return {"filename": file.filename}

# Faz o upload de varias imagens
@app.post("/users/{user_id}/images/uploadfiles/")
async def create_upload_files(user_id:str, files: List[UploadFile] = File(...)):
    print(f"Uploading multiplefiles fo {user_id}")
    for img in files:
        with open(f'{img.filename}', "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
    return {"filename": img.filename}

@app.delete("/users/{user_id}/images/{image_id}")
def delete_image_from_user(user_id: int, image_id:int, db: Session = Depends(get_db)):
    user_image = crud.delete_image(db, user_id, image_id)
    return {"msg":"imagem deletada"}