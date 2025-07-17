import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from typing import Dict, List, Optional
from decimal import Decimal
import uuid
from datetime import datetime
import os

class DynamoDBClient:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        self.table_name = os.getenv('EXPENSES_TABLE', 'expenses-table')
        self.table = self.dynamodb.Table(self.table_name)
    
    def create_expense(self, expense_data: Dict) -> Dict:
        """Create a new expense record"""
        try:
            expense_id = str(uuid.uuid4())
            now = datetime.now()
            
            item = {
                'expense_id': expense_id,
                'service_name': expense_data['service_name'],
                'client': expense_data['client'],
                'cost': Decimal(str(expense_data['cost'])),
                'date': expense_data['date'].isoformat(),
                'description': expense_data.get('description'),
                'created_at': now.isoformat(),
                'updated_at': now.isoformat()
            }
            
            response = self.table.put_item(Item=item)
            return item
            
        except ClientError as e:
            raise Exception(f"Failed to create expense: {e.response['Error']['Message']}")
    
    def get_expense(self, expense_id: str) -> Optional[Dict]:
        """Get expense by ID"""
        try:
            response = self.table.get_item(Key={'expense_id': expense_id})
            return response.get('Item')
            
        except ClientError as e:
            raise Exception(f"Failed to get expense: {e.response['Error']['Message']}")
    
    def update_expense(self, expense_id: str, update_data: Dict) -> Dict:
        """Update an existing expense"""
        try:
            # Build update expression
            update_expression = "SET updated_at = :updated_at"
            expression_values = {':updated_at': datetime.now().isoformat()}
            
            for key, value in update_data.items():
                if value is not None:
                    if key == 'cost':
                        value = Decimal(str(value))
                    update_expression += f", {key} = :{key}"
                    expression_values[f":{key}"] = value
            
            response = self.table.update_item(
                Key={'expense_id': expense_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues='ALL_NEW'
            )
            
            return response['Attributes']
            
        except ClientError as e:
            raise Exception(f"Failed to update expense: {e.response['Error']['Message']}")
    
    def delete_expense(self, expense_id: str) -> bool:
        """Delete an expense"""
        try:
            self.table.delete_item(Key={'expense_id': expense_id})
            return True
            
        except ClientError as e:
            raise Exception(f"Failed to delete expense: {e.response['Error']['Message']}")
    
    def list_expenses(self, limit: int = 50) -> List[Dict]:
        """List all expenses with pagination"""
        try:
            response = self.table.scan(Limit=limit)
            return response.get('Items', [])
            
        except ClientError as e:
            raise Exception(f"Failed to list expenses: {e.response['Error']['Message']}")
