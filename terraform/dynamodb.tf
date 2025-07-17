resource "aws_dynamodb_table" "expenses_table" {
  name           = var.table_name
  billing_mode   = "PAY_PER_REQUEST"  # Free tier friendly
  hash_key       = "expense_id"
  
  attribute {
    name = "expense_id"
    type = "S"
  }
  
  # Global Secondary Index for querying by client
  global_secondary_index {
    name            = "client-index"
    hash_key        = "client"
    projection_type = "ALL"
  }
  
  attribute {
    name = "client"
    type = "S"
  }
  
  # Global Secondary Index for querying by service
  global_secondary_index {
    name            = "service-index"
    hash_key        = "service_name"
    projection_type = "ALL"
  }
  
  attribute {
    name = "service_name"
    type = "S"
  }
  
  tags = {
    Name        = "${var.project_name}-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
  }
}
