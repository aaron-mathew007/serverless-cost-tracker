from fastapi import HTTPException, status
from boto3.dynamodb.conditions import Key
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from collections import defaultdict
import calendar

from src.database.dynamodb_client import DynamoDBClient

class CostAnalysisHandler:
    def __init__(self):
        self.db_client = DynamoDBClient()
    
    def get_cost_breakdown(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        group_by: str = "service",
        client_filter: Optional[str] = None
    ) -> Dict:
        """Get cost breakdown by service, client, or time period"""
        try:
            # Set default date range (last 30 days)
            if not end_date:
                end_date = datetime.now()
            if not start_date:
                start_date = end_date - timedelta(days=30)
            
            # Get all expenses
            expenses = self.db_client.list_expenses(limit=1000)
            
            # Filter by date range
            filtered_expenses = self._filter_by_date_range(expenses, start_date, end_date)
            
            # Filter by client if specified
            if client_filter:
                filtered_expenses = [
                    exp for exp in filtered_expenses 
                    if exp.get('client', '').lower() == client_filter.lower()
                ]
            
            # Group expenses
            breakdown = self._group_expenses(filtered_expenses, group_by)
            
            # Calculate totals
            total_cost = sum(float(exp.get('cost', 0)) for exp in filtered_expenses)
            total_count = len(filtered_expenses)
            
            return {
                "summary": {
                    "total_cost": round(total_cost, 2),
                    "total_expenses": total_count,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "group_by": group_by
                },
                "breakdown": breakdown
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get cost breakdown: {str(e)}"
            )
    
    def get_monthly_trends(self, months: int = 6) -> Dict:
        """Get monthly cost trends"""
        try:
            # Get expenses for the last N months
            end_date = datetime.now()
            start_date = end_date - timedelta(days=months * 30)
            
            expenses = self.db_client.list_expenses(limit=1000)
            filtered_expenses = self._filter_by_date_range(expenses, start_date, end_date)
            
            # Group by month
            monthly_data = defaultdict(lambda: {"total_cost": 0, "count": 0})
            
            for expense in filtered_expenses:
                expense_date = datetime.fromisoformat(expense['date'])
                month_key = expense_date.strftime("%Y-%m")
                
                monthly_data[month_key]["total_cost"] += float(expense.get('cost', 0))
                monthly_data[month_key]["count"] += 1
            
            # Format response
            trends = []
            for month_key in sorted(monthly_data.keys()):
                year, month = month_key.split('-')
                month_name = calendar.month_name[int(month)]
                
                trends.append({
                    "month": f"{month_name} {year}",
                    "total_cost": round(monthly_data[month_key]["total_cost"], 2),
                    "expense_count": monthly_data[month_key]["count"]
                })
            
            return {
                "trends": trends,
                "period": f"Last {months} months"
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get monthly trends: {str(e)}"
            )
    
    def get_top_services(self, limit: int = 10) -> List[Dict]:
        """Get top services by cost"""
        try:
            expenses = self.db_client.list_expenses(limit=1000)
            
            # Group by service
            service_costs = defaultdict(lambda: {"total_cost": 0, "count": 0})
            
            for expense in expenses:
                service_name = expense.get('service_name', 'Unknown')
                service_costs[service_name]["total_cost"] += float(expense.get('cost', 0))
                service_costs[service_name]["count"] += 1
            
            # Sort by total cost
            top_services = sorted(
                [
                    {
                        "service_name": service,
                        "total_cost": round(data["total_cost"], 2),
                        "expense_count": data["count"]
                    }
                    for service, data in service_costs.items()
                ],
                key=lambda x: x["total_cost"],
                reverse=True
            )
            
            return top_services[:limit]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get top services: {str(e)}"
            )
    
    def _filter_by_date_range(self, expenses: List[Dict], start_date: datetime, end_date: datetime) -> List[Dict]:
        """Filter expenses by date range"""
        filtered = []
        for expense in expenses:
            expense_date = datetime.fromisoformat(expense['date'])
            if start_date <= expense_date <= end_date:
                filtered.append(expense)
        return filtered
    
    def _group_expenses(self, expenses: List[Dict], group_by: str) -> List[Dict]:
        """Group expenses by specified field"""
        grouped = defaultdict(lambda: {"total_cost": 0, "count": 0, "expenses": []})
        
        for expense in expenses:
            key = expense.get(group_by, 'Unknown')
            grouped[key]["total_cost"] += float(expense.get('cost', 0))
            grouped[key]["count"] += 1
            grouped[key]["expenses"].append(expense)
        
        return [
            {
                "category": category,
                "total_cost": round(data["total_cost"], 2),
                "expense_count": data["count"],
                "percentage": round((data["total_cost"] / sum(float(exp.get('cost', 0)) for exp in expenses)) * 100, 2) if expenses else 0
            }
            for category, data in grouped.items()
        ]
