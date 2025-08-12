from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database, crud, models, schemas

router = APIRouter(prefix="/roles", tags=["Roles"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=models.RoleOut)
def create(role: models.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db, role)

@router.put("/{role_id}", response_model=models.RoleOut)
def update(role_id: int, role: models.RoleUpdate, db: Session = Depends(get_db)):
    updated = crud.update_role(db, role_id, role)
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated

@router.delete("/{role_id}")
def delete(role_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_role(db, role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted"}

@router.get("/", response_model=list[models.RoleOut])
def get_all(db: Session = Depends(get_db)):
    return crud.get_roles(db)

@router.get("/{role_id}", response_model=models.RoleOut)
def get_by_id(role_id: int, db: Session = Depends(get_db)):
    role = crud.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role