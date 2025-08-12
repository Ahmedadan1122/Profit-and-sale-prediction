from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import ml_model, database, models
from app.models import PredictionInput
from app import schemas


import pandas as pd
from datetime import datetime

router = APIRouter(prefix="/predict", tags=["Predictions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def predict(input_data: PredictionInput, db: Session = Depends(get_db)):
    try:
        model = ml_model.load_model()
        input_dict = input_data.dict()

        base_input = pd.DataFrame([{
            "Year": input_dict["year"] + 1,
            "Month Number": input_dict["month"],
            "Units Sold": input_dict["units_sold"],
            "Sale Price": input_dict["sale_price"],
            "COGS": input_dict["cogs"]
        }])

      

        sales, profit = ml_model.predict(model, base_input)

        prediction = schemas.Prediction(
            year=input_dict["year"] + 1,
            month=input_dict["month"],
            units_sold=input_dict["units_sold"],
            sale_price=input_dict["sale_price"],
            cogs=input_dict["cogs"],
            predicted_sales=float(sales[0]),
            predicted_profit=float(profit[0]),
            user_id=input_data.user_id,
            created_at=datetime.utcnow()
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        return {
            "message": "Prediction successful",
            "predicted_sales": round(sales[0], 2),
            "predicted_profit": round(profit[0], 2)
        }

    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="No model selected yet.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))