from sqlalchemy.orm import Session
from app.schemas import User, Prediction
from passlib.hash import bcrypt

def create_user(db: Session, name: str, email: str, password: str):
    hashed_password = bcrypt.hash(password)
    db_user = User(name=name, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, updates: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in updates.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def create_prediction(db: Session, user_id: int, input_data: dict, output_data: dict):
    prediction = Prediction(
        year=input_data["year"],
        month=input_data["month"],
        units_sold=input_data["units_sold"],
        sale_price=input_data["sale_price"],
        cogs=input_data["cogs"],
        predicted_sales=output_data["predicted_sales"],
        predicted_profit=output_data["predicted_profit"],
        user_id=user_id
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

def get_user_predictions(db: Session, user_id: int):
    return db.query(Prediction).filter(Prediction.user_id == user_id).all()

def get_predictions(db: Session):
    return db.query(Prediction).all()

def get_predictions_by_user(db: Session, user_id: int):
    return db.query(Prediction).filter(Prediction.user_id == user_id).all()

from sqlalchemy.orm import Session
from app.schemas import Role
from app.models import RoleCreate, RoleUpdate

def create_role(db: Session, role: RoleCreate):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role: RoleUpdate):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role:
        db_role.name = role.name
        db.commit()
        db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role

def get_roles(db: Session):
    return db.query(Role).all()

def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()
