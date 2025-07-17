# Error Handling Guide

## Common Lambda + DynamoDB Pitfalls

### 1. Cold Start Issues

**Problem**: Lambda cold starts can cause timeouts
**Solution**: 
- Optimize package size
- Use provisioned concurrency for critical paths
- Implement proper timeout handling

Configure timeout in Terraform
resource "aws_lambda_function" "cost_tracker_api" {
timeout = 30 # Adjust based on needs
memory_size = 512 # More memory = faster cold starts
}


### 2. DynamoDB Throttling

**Problem**: Too many requests can cause throttling
**Solution**:
- Use PAY_PER_REQUEST billing mode
- Implement exponential backoff
- Monitor CloudWatch metrics

Implement retry logic
import time
from botocore.exceptions import ClientError

def retry_dynamodb_operation(operation, max_retries=3):
for attempt in range(max_retries):
try:
return operation()
except ClientError as e:
if e.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
wait_time = (2 ** attempt) * 0.1 # Exponential backoff
time.sleep(wait_time)
continue
raise

### 3. Memory and Timeout Tuning

**Lambda Memory Configuration**:
- 128MB: Basic operations (cold start ~1-2s)
- 512MB: Recommended for FastAPI (cold start ~500ms)
- 1024MB: Heavy operations (cold start ~200ms)

**Timeout Guidelines**:
- Simple CRUD: 10-15 seconds
- Complex analytics: 30-60 seconds
- File processing: 5-15 minutes

### 4. Connection Pooling

**Problem**: Too many DynamoDB connections
**Solution**: Reuse connections across invocations

Global connection (outside handler)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('expenses-table')

def lambda_handler(event, context):
# Reuse existing connection
response = table.get_item(Key={'id': 'some-id'})
return response


### 5. Error Response Standards

**HTTP Status Codes**:
- 200: Success
- 201: Created
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid API key)
- 404: Not Found
- 500: Internal Server Error

**Error Response Format**:

{
"error": {
"code": "EXPENSE_NOT_FOUND",
"message": "Expense with ID 12345 not found",
"details": {
"expense_id": "12345",
"timestamp": "2024-01-15T10:30:00Z"
}
}
}



### 6. Monitoring and Alerting

**CloudWatch Alarms**:
- Lambda duration > 25 seconds
- Lambda errors > 1%
- DynamoDB throttled requests > 0
- API Gateway 5XX errors > 5%

**Cost Monitoring**:
- Set up billing alerts
- Monitor DynamoDB consumed capacity
- Track Lambda invocation counts
