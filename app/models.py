from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    role: Optional[str]
    is_blocked: Optional[int]

class PredictionInput(BaseModel):
    year: int
    month: int
    units_sold: float
    sale_price: float
    cogs: float
    user_id: int

class PredictionResult(BaseModel):
    predicted_sales: float
    predicted_profit: float

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int

    class Config:
        orm_mode = True
