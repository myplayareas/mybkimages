from sqlalchemy.orm import Session
from . import models, schemas

# Todo: tratar as excecoes

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, fullname=user.fullname, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_images(db: Session):
    return db.query(models.Image).all()

def get_images_from_user(db: Session, user_id:int):
    return db.query(models.Image).filter(models.Image.owner_id == user_id).all()

def get_image_from_user(db: Session, user_id:int, image_id):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

def create_user_image(db: Session, image: schemas.ImageCreate, user_id: int):
    db_image = models.Image(**image.dict(), owner_id=user_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def delete_image(db: Session, user_id:int, image_id: int):
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    db.delete(db_image)
    db.commit()
    return db_image