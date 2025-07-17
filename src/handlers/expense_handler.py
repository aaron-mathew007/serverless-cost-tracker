from fastapi import HTTPException, status
from typing import List
from src.models.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from src.database.dynamodb_client import DynamoDBClient
from decimal import Decimal
from datetime import datetime

class ExpenseHandler:
    def __init__(self):
        self.db_client = DynamoDBClient()
    
    def create_expense(self, expense: ExpenseCreate) -> ExpenseResponse:
        """Create a new expense"""
        try:
            expense_data = expense.dict()
            created_expense = self.db_client.create_expense(expense_data)
            return self._format_response(created_expense)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create expense: {str(e)}"
            )
    
    def get_expense(self, expense_id: str) -> ExpenseResponse:
        """Get expense by ID"""
        try:
            expense = self.db_client.get_expense(expense_id)
            if not expense:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Expense with ID {expense_id} not found"
                )
            
            return self._format_response(expense)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get expense: {str(e)}"
            )
    
    def update_expense(self, expense_id: str, expense_update: ExpenseUpdate) -> ExpenseResponse:
        """Update an existing expense"""
        try:
            # Check if expense exists
            existing_expense = self.db_client.get_expense(expense_id)
            if not existing_expense:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Expense with ID {expense_id} not found"
                )
            
            update_data = expense_update.dict(exclude_unset=True)
            updated_expense = self.db_client.update_expense(expense_id, update_data)
            return self._format_response(updated_expense)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update expense: {str(e)}"
            )
    
    def delete_expense(self, expense_id: str) -> dict:
        """Delete an expense"""
        try:
            # Check if expense exists
            existing_expense = self.db_client.get_expense(expense_id)
            if not existing_expense:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Expense with ID {expense_id} not found"
                )
            
            self.db_client.delete_expense(expense_id)
            return {"message": f"Expense {expense_id} deleted successfully"}
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete expense: {str(e)}"
            )
    
    def list_expenses(self, limit: int = 50) -> List[ExpenseResponse]:
        """List all expenses"""
        try:
            expenses = self.db_client.list_expenses(limit)
            return [self._format_response(expense) for expense in expenses]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to list expenses: {str(e)}"
            )
    
    def _format_response(self, expense: dict) -> ExpenseResponse:
        """Format database response to Pydantic model"""
        return ExpenseResponse(
            expense_id=expense['expense_id'],
            service_name=expense['service_name'],
            client=expense['client'],
            cost=float(expense['cost']),
            date=datetime.fromisoformat(expense['date']),
            description=expense.get('description'),
            created_at=datetime.fromisoformat(expense['created_at']),
            updated_at=datetime.fromisoformat(expense['updated_at'])
        )
