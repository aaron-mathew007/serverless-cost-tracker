from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from decimal import Decimal
import uuid

class ExpenseBase(BaseModel):
    service_name: str = Field(..., min_length=1, max_length=100)
    client: str = Field(..., min_length=1, max_length=50)
    cost: Decimal = Field(..., gt=0, le=100000)
    date: datetime = Field(default_factory=datetime.now)
    description: Optional[str] = Field(None, max_length=500)
    
    @validator('cost')
    def validate_cost(cls, v):
        if v <= 0:
            raise ValueError('Cost must be positive')
        return round(v, 2)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    service_name: Optional[str] = Field(None, min_length=1, max_length=100)
    client: Optional[str] = Field(None, min_length=1, max_length=50)
    cost: Optional[Decimal] = Field(None, gt=0, le=100000)
    description: Optional[str] = Field(None, max_length=500)

class ExpenseResponse(ExpenseBase):
    expense_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
