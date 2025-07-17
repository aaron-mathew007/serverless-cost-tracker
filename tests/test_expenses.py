import pytest
from fastapi.testclient import TestClient
from moto import mock_dynamodb
import boto3
from src.main import app

client = TestClient(app)

@mock_dynamodb
def test_create_expense():
    # Setup mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='expenses-table',
        KeySchema=[
            {'AttributeName': 'expense_id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'expense_id', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    
    # Test data
    expense_data = {
        "service_name": "EC2",
        "client": "test-client",
        "cost": 25.50,
        "description": "Test expense"
    }
    
    # Test create expense
    response = client.post("/expenses", json=expense_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["service_name"] == "EC2"
    assert data["client"] == "test-client"
    assert data["cost"] == 25.50

@mock_dynamodb
def test_get_expense():
    # Setup mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='expenses-table',
        KeySchema=[
            {'AttributeName': 'expense_id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'expense_id', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    
    # Test get non-existent expense
    response = client.get("/expenses/non-existent-id")
    assert response.status_code == 404

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "Cost Tracker API is running"}
