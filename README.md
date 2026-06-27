# AWS EBS Snapshot Cleanup Lambda

A serverless AWS Lambda function built with Python and boto3 to automatically identify and delete unused EBS snapshots, helping reduce unnecessary storage costs.

## Features

- Lists EC2 instances
- Identifies EBS snapshots owned by the AWS account
- Checks whether the associated EBS volume exists
- Verifies whether the volume is attached to an EC2 instance
- Deletes snapshots associated with deleted or detached volumes
- Configurable snapshot retention period
- Exception handling using botocore
- CloudWatch logging
- EventBridge scheduled execution

## Tech Stack

- AWS Lambda
- Amazon EC2
- Amazon EBS
- Amazon EventBridge
- Amazon CloudWatch
- IAM
- Python
- boto3

## Architecture

EventBridge
↓
Lambda
↓
EC2 / EBS APIs
↓
Delete unused snapshots
↓
CloudWatch Logs

## Required IAM Permissions

- ec2:DescribeInstances
- ec2:DescribeVolumes
- ec2:DescribeSnapshots
- ec2:DeleteSnapshot

## Deployment

1. Create a Lambda function.
2. Upload the Python code.
3. Attach the IAM policy.
4. Create an EventBridge schedule.
5. Monitor execution in CloudWatch Logs.

## Author

Anurag Sahu
