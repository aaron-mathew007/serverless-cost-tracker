# 🚀 Serverless Cost Tracker API

[![AWS](https://img.shields.io/badge/AWS-Free%20Tier-orange)](https://aws.amazon.com/free/)
[![Terraform](https://img.shields.io/badge/Terraform-Infrastructure%20as%20Code-blue)](https://www.terraform.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python%20API-green)](https://fastapi.tiangolo.com/)
[![DynamoDB](https://img.shields.io/badge/DynamoDB-NoSQL%20Database-red)](https://aws.amazon.com/dynamodb/)

> **A production-ready serverless API for tracking AWS costs and expenses, built with FastAPI, AWS Lambda, and DynamoDB.**

## 🌟 Features

- ✅ **Serverless Architecture**: Built on AWS Lambda for automatic scaling
- ✅ **NoSQL Database**: DynamoDB for high-performance data storage
- ✅ **Infrastructure as Code**: Complete Terraform configuration
- ✅ **API Authentication**: Secure API key-based authentication
- ✅ **Cost Analysis**: Advanced cost breakdown and trend analysis
- ✅ **Free Tier Optimized**: Designed to run within AWS Free Tier limits
- ✅ **Production Ready**: Comprehensive error handling and logging

## 🏗️ Architecture


<img width="930" height="358" alt="image" src="https://github.com/user-attachments/assets/ca601d4f-0460-4152-b145-2343586db70f" />



## 🚀 Quick Start

### Prerequisites

- AWS CLI configured
- Terraform >= 1.0
- Python 3.9+
- Docker (for SAM testing)

### 1. Clone Repository
git clone https://github.com/aaron-mathew007/serverless-cost-tracker.git

cd serverless-cost-tracker


### 2. Deploy Infrastructure


Navigate to Terraform directory
cd terraform

Initialize Terraform
terraform init

Plan deployment
terraform plan

Apply infrastructure
terraform apply

Build and deploy
chmod +x build_and_deploy.sh
./build_and_deploy.sh


### 4. Test API

Health check
curl https://your-api-gateway-url/health

Create expense
curl -X POST https://your-api-gateway-url/expenses
-H "Content-Type: application/json"
-H "X-API-Key: your-api-key"
-d '{
"service_name": "EC2",
"client": "production",
"cost": 25.50,
"description": "Monthly EC2 instance cost"
}'




## 📊 API Endpoints

### Core Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | Health check | ❌ |
| POST | `/expenses` | Create expense | ✅ |
| GET | `/expenses/{id}` | Get expense | ✅ |
| PUT | `/expenses/{id}` | Update expense | ✅ |
| DELETE | `/expenses/{id}` | Delete expense | ✅ |
| GET | `/expenses` | List expenses | ✅ |

### Analytics Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/cost-breakdown` | Cost breakdown analysis | ✅ |
| GET | `/monthly-trends` | Monthly cost trends | ✅ |
| GET | `/top-services` | Top services by cost | ✅ |

## 🔐 Authentication

The API uses API key authentication. Include the API key in the request header:


curl -H "X-API-Key: your-api-key" https://your-api-gateway-url/expenses



## 🧪 Testing

### Local Testing

Install dependencies
pip install -r requirements.txt

Run tests
pytest tests/

Test with SAM CLI
sam build
sam local start-api



### Load Testing

Install Locust
pip install locust

Run load tests
locust -f tests/locust_load_test.py


## 💰 Cost Analysis

### AWS Free Tier Usage

| Service | Free Tier Limit | Estimated Usage |
|---------|----------------|-----------------|
| Lambda | 1M requests/month | ~10K requests |
| DynamoDB | 25GB storage | ~1GB storage |
| API Gateway | 1M requests/month | ~10K requests |
| CloudWatch | 5GB logs | ~100MB logs |

**Estimated Monthly Cost**: $0.00 (within free tier)

### Production Scaling

For production workloads exceeding free tier:
- Lambda: ~$0.20 per 1M requests
- DynamoDB: ~$0.25 per GB/month
- API Gateway: ~$3.50 per million requests

## 🔧 Configuration

### Environment Variables

Required
AWS_REGION=us-east-1
EXPENSES_TABLE=expenses-table

Optional
API_KEY=your-secret-api-key
LOG_LEVEL=INFO


### Terraform Variables

terraform/terraform.tfvars
aws_region = "us-east-1"
project_name = "serverless-cost-tracker"
environment = "prod"


## 📈 Monitoring

### CloudWatch Metrics

- Lambda invocations and duration
- DynamoDB read/write capacity
- API Gateway response times
- Error rates and logs

### Custom Alerts

Create billing alarm
aws cloudwatch put-metric-alarm
--alarm-name "HighCosts"
--alarm-description "Alert when costs exceed $10"
--metric-name EstimatedCharges
--namespace AWS/Billing
--statistic Maximum
--period 86400
--threshold 10
--comparison-operator GreaterThanThreshold


## 🚀 Deployment

### CI/CD Pipeline

.github/workflows/deploy.yml
name: Deploy to AWS

on:
push:
branches: [main]

jobs:
deploy:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v2
- name: Configure AWS credentials
uses: aws-actions/configure-aws-credentials@v1
with:
aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
aws-region: us-east-1
- name: Deploy with Terraform
run: |
cd terraform
terraform init
terraform apply -auto-approve


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [AWS Free Tier](https://aws.amazon.com/free/) - Free cloud services
- [Terraform](https://www.terraform.io/) - Infrastructure as Code
- [Mangum](https://mangum.io/) - ASGI adapter for AWS Lambda

---

**⭐ If this project helped you, please give it a star!**

