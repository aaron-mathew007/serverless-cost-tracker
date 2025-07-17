# Create SNS topic for cost alerts
resource "aws_sns_topic" "cost_alerts" {
  name = "${var.project_name}-cost-alerts"
  
  tags = {
    Name        = "${var.project_name}-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
  }
}

# Create SNS topic subscription
resource "aws_sns_topic_subscription" "cost_alerts_email" {
  topic_arn = aws_sns_topic.cost_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# Create CloudWatch alarm for high costs
resource "aws_cloudwatch_metric_alarm" "high_cost_alarm" {
  alarm_name          = "${var.project_name}-high-cost-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "EstimatedCharges"
  namespace           = "AWS/Billing"
  period              = "86400"
  statistic           = "Maximum"
  threshold           = "10"
  alarm_description   = "This metric monitors AWS estimated charges"
  alarm_actions       = [aws_sns_topic.cost_alerts.arn]

  dimensions = {
    Currency = "USD"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
  }
}

# Lambda function for cost analysis
resource "aws_lambda_function" "cost_monitor" {
  filename         = data.archive_file.cost_monitor_zip.output_path
  function_name    = "${var.project_name}-cost-monitor"
  role            = aws_iam_role.cost_monitor_role.arn
  handler         = "cost_monitor.handler"
  runtime         = "python3.9"
  timeout         = 60

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.cost_alerts.arn
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.cost_monitor_policy,
  ]
}

# IAM role for cost monitor Lambda
resource "aws_iam_role" "cost_monitor_role" {
  name = "${var.project_name}-cost-monitor-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM policy for cost monitor
resource "aws_iam_policy" "cost_monitor_policy" {
  name        = "${var.project_name}-cost-monitor-policy"
  description = "Policy for cost monitor Lambda"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ce:GetCostAndUsage",
          "ce:GetUsageReport",
          "sns:Publish"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "cost_monitor_policy" {
  role       = aws_iam_role.cost_monitor_role.name
  policy_arn = aws_iam_policy.cost_monitor_policy.arn
}

# Create deployment package for cost monitor
data "archive_file" "cost_monitor_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/cost_monitor"
  output_path = "${path.module}/../cost_monitor.zip"
}

# Schedule cost monitor to run daily
resource "aws_cloudwatch_event_rule" "daily_cost_check" {
  name                = "${var.project_name}-daily-cost-check"
  description         = "Run cost monitor daily"
  schedule_expression = "rate(1 day)"
}

# Connect CloudWatch event to Lambda
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_cost_check.name
  target_id = "CostMonitorLambdaTarget"
  arn       = aws_lambda_function.cost_monitor.arn
}

# Grant permission for CloudWatch to invoke Lambda
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cost_monitor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_cost_check.arn
}
