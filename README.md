# AWS EBS Snapshot Cleanup Lambda

A production-inspired AWS Lambda function built with **Python** and **boto3** to automatically identify and delete unused Amazon EBS snapshots. The solution helps optimize AWS storage costs by removing snapshots whose associated volumes have been deleted or are no longer attached to an EC2 instance.

---

# Features

* Automatically discovers all EBS snapshots owned by the AWS account.
* Lists all running and stopped EC2 instances.
* Retrieves EBS volume information using the EC2 API.
* Deletes snapshots whose associated volume no longer exists.
* Deletes snapshots whose associated volume is detached from all EC2 instances.
* Supports configurable snapshot retention period.
* Handles AWS API exceptions gracefully.
* Generates detailed execution logs in Amazon CloudWatch.
* Can be scheduled using Amazon EventBridge for automatic execution.

---

# Architecture

```
                Amazon EventBridge
                       │
                       ▼
                AWS Lambda Function
                       │
                       ▼
                  boto3 (EC2 API)
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Describe       Describe      Describe
   Instances      Volumes       Snapshots
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
          Validate Snapshot Ownership
                       │
                       ▼
      Delete Unused EBS Snapshots
                       │
                       ▼
             Amazon CloudWatch Logs
```

---

# Project Structure

```
aws-ebs-snapshot-cleanup-lambda/
│
├── lambda_function.py
├── requirements.txt
├── iam-policy.json
├── README.md
├── .gitignore
└── LICENSE (Optional)
```

---

# Technologies Used

* AWS Lambda
* Amazon EC2
* Amazon EBS
* Amazon EventBridge
* Amazon CloudWatch
* AWS IAM
* Python 3.14
* boto3
* botocore

---

# Workflow

1. EventBridge triggers the Lambda function on a schedule.
2. Lambda retrieves all EC2 instances.
3. Lambda retrieves all EBS snapshots owned by the account.
4. Lambda checks whether the associated EBS volume exists.
5. Lambda verifies whether the volume is attached to an EC2 instance.
6. Snapshots associated with deleted or detached volumes are removed.
7. Execution logs and cleanup summary are written to CloudWatch.

---

# Prerequisites

* AWS Account
* Python 3.14
* boto3
* AWS CLI configured
* IAM Role with EC2 permissions

---

# IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeSnapshots",
        "ec2:DescribeVolumes",
        "ec2:DeleteSnapshot"
      ],
      "Resource": "*"
    }
  ]
}
```

---

# Deployment Steps

## Step 1

Create a new AWS Lambda function.

Runtime:

```
Python 3.14
```

---

## Step 2

Upload the `lambda_function.py` source code.

---

## Step 3

Attach the required IAM Role.

---

## Step 4

Configure the Lambda handler.

```
lambda_function.lambda_handler
```

---

## Step 5

Create an Amazon EventBridge Rule.

Example Schedule:

```
rate(1 day)
```

---

## Step 6

Monitor execution using CloudWatch Logs.

---

# Example Output

```
================================================================================
Starting EBS Snapshot Cleanup
================================================================================

EC2 Instance Inventory

Instance Name : Production-Web
Instance ID   : i-0123456789abcdef0
State         : running

--------------------------------------------------------------------------------

Snapshot ID : snap-0123456789abcdef
Volume ID   : vol-0123456789abcdef

Deleted : Volume no longer exists.

================================================================================
Cleanup Summary
================================================================================

Snapshots Scanned : 12
Deleted           : 4
Skipped           : 8
Failed            : 0
```

---

# Cost Optimization

This project helps reduce unnecessary AWS storage costs by automatically removing:

* Snapshots whose associated EBS volume has been deleted.
* Snapshots whose associated EBS volume is detached from any EC2 instance.

---

# Future Improvements

* Pagination support for large AWS environments.
* SNS email notifications after cleanup.
* Configurable retention period using Lambda Environment Variables.
* Tag-based snapshot protection.
* Multi-region snapshot cleanup.
* CloudWatch metrics and dashboards.
* Unit testing using moto.
* Infrastructure as Code deployment using Terraform or AWS SAM.

---


# Requirements

```
boto3
botocore
```

---


# Author

**Anurag Sahu**

If you found this project helpful, consider giving it a ⭐ on GitHub.
