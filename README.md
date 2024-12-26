# Serverless Email Verification Function

## Overview
This repository contains a Lambda function designed to enable **SendGrid** for email verification. The function handles user email verification efficiently using AWS Lambda and integrates with **SNS** for streamlined communication.

## Key Features

- **SendGrid Integration**: Facilitates email-based user verification.  
- **AWS Lambda**: Serverless architecture for cost-efficient and scalable execution.  
- **SNS Integration**: Simplifies communication and improves reliability for user verification workflows.  
- **Customizable**: Easily adaptable for other email services if required.  

### Please check the Terraform repository for the reusable Infrastructure code here:
https://github.com/surjith1610/terraform-webapp-infrastructure

### Please check the Web application repository which will be deployed using the reusable Infrastructure code here:
https://github.com/surjith1610/cloud-webapplication

## Prerequisites
Before deploying this function using **Terraform**, follow these steps to ensure the environment is properly set up:

1. Install the required dependencies using `pip3`:
   ```bash
   pip3 install -r requirements.txt -t .

2. Zip the Lambda function code along with the installed dependencies before uploading it through the Terraform configuration.
