import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.ml_model import clean_dataset, train_and_compare_models, save_selected_model
from app.crud import (
    get_all_users, update_user, delete_user,
    get_predictions, get_predictions_by_user
)
from app.models import UserUpdate
router = APIRouter()
UPLOAD_DIR = "data/uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        df = clean_dataset(file_path)
        results = train_and_compare_models(df)

        return {
            "message": "Dataset uploaded and models trained successfully.",
            "file_path": file_path,
            "models": {
                k: {
                    "name": v["name"],
                    "sales_mse": v["sales_mse"],
                    "profit_mse": v["profit_mse"],
                    "sales_accuracy": v["sales_accuracy"],
                    "profit_accuracy": v["profit_accuracy"]
                } for k, v in results.items()
            },
            "instruction": "Use POST /admin/select-model with {'model_number': 1-4} to choose the model"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ModelSelect(BaseModel):
    model_number: int

@router.post("/select-model")
def select_model(data: ModelSelect):
    try:
        save_selected_model(data.model_number)
        return {"message": f"Model #{data.model_number} has been selected for future predictions."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.patch("/users/{user_id}")
def modify_user(user_id: int, updates: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, updates.dict(exclude_unset=True))

@router.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)

@router.get("/predictions")
def read_all_predictions(db: Session = Depends(get_db)):
    return get_predictions(db)

@router.get("/predictions/user/{user_id}")
def read_predictions_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_predictions_by_user(db, user_id)