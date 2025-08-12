from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, admin, predictions,roles

app = FastAPI(title="Sales & Profit Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(predictions.router, prefix="/predict", tags=["Predictions"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])
