from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from typing import List

from src.models.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from src.handlers.expense_handler import ExpenseHandler

# Initialize FastAPI app
app = FastAPI(
    title="Serverless Cost Tracker API",
    description="A serverless API for tracking AWS costs and expenses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize handler
expense_handler = ExpenseHandler()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Cost Tracker API is running"}

# Expense endpoints
@app.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(expense: ExpenseCreate):
    """Create a new expense record"""
    return expense_handler.create_expense(expense)

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
async def get_expense(expense_id: str):
    """Get expense by ID"""
    return expense_handler.get_expense(expense_id)

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
async def update_expense(expense_id: str, expense_update: ExpenseUpdate):
    """Update an existing expense"""
    return expense_handler.update_expense(expense_id, expense_update)

@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: str):
    """Delete an expense"""
    return expense_handler.delete_expense(expense_id)

@app.get("/expenses", response_model=List[ExpenseResponse])
async def list_expenses(limit: int = 50):
    """List all expenses"""
    return expense_handler.list_expenses(limit)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# Lambda handler
handler = Mangum(app)
