# -Serverless-Architecture-Assignment
This assignment is to show different task on  Serverless Architecture using BOTO3 and Lambda function.

 AWS Serverless Assignments using Lambda & Boto3

This repository contains multiple AWS serverless automation assignments using **AWS Lambda, Boto3, and AWS services like EC2, EBS, and Amazon Comprehend**.

---

#  Assignment 1: Automated EC2 Instance Management

##  Objective
Automatically start and stop EC2 instances based on tags.

## Tags Used
- `Action = Auto-Start`
- `Action = Auto-Stop`

##  Lambda Function Code

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Stop instances
    stop_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}]
    )

    stop_ids = [
        instance['InstanceId']
        for reservation in stop_response['Reservations']
        for instance in reservation['Instances']
    ]

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Stopped instances: {stop_ids}")

    # Start instances
    start_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}]
    )

    start_ids = [
        instance['InstanceId']
        for reservation in start_response['Reservations']
        for instance in reservation['Instances']
    ]

    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Started instances: {start_ids}")

    return {
        'statusCode': 200,
        'body': 'EC2 instances processed successfully'
    }
____________________________________________________________________________________________
____________________________________________________________________________________________


Assignment 4: Automatic EBS Snapshot & Cleanup
 Objective

Create EBS snapshots and delete old snapshots automatically.

 Lambda Function Code

import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    VOLUME_ID = 'your-volume-id'
    RETENTION_DAYS = 0

    # Create snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated snapshot created by Lambda'
    )

    print(f"Created snapshot: {snapshot['SnapshotId']}")

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)

    snapshots = ec2.describe_snapshots(OwnerIds=['self'])

    for snap in snapshots['Snapshots']:
        if snap['StartTime'] < cutoff_date:
            ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
            print(f"Deleted snapshot: {snap['SnapshotId']}")

    return {
        'statusCode': 200,
        'body': 'Snapshot cleanup completed'
    }


_______________________________________________________________________________________________
_______________________________________________________________________________________________


Assignment 5: Auto-Tagging EC2 Instances
 Objective

Automatically tag EC2 instances at launch.

Lambda Function Code


import boto3
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    instance_id = event['detail']['instance-id']
    launch_date = datetime.utcnow().strftime('%Y-%m-%d')

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {'Key': 'LaunchDate', 'Value': launch_date},
            {'Key': 'CreatedBy', 'Value': 'Lambda'}
        ]
    )

    print(f'Tags added to instance {instance_id}')

    return {
        'statusCode': 200,
        'body': f'Tags added to {instance_id}'
    }



_____________________________________________________________________________________________________
_____________________________________________________________________________________________________



Assignment 8: Sentiment Analysis using Amazon Comprehend
 Objective

Analyze sentiment of user reviews using AWS AI service.

 Service Used
Amazon Comprehend
 Lambda Function Code

import json
import boto3

comprehend = boto3.client('comprehend')

def lambda_handler(event, context):

    review_text = event.get('review', '')

    if not review_text:
        return {
            'statusCode': 400,
            'body': json.dumps('No review text provided')
        }

    response = comprehend.detect_sentiment(
        Text=review_text,
        LanguageCode='en'
    )

    sentiment = response['Sentiment']

    print(f"Review: {review_text}")
    print(f"Sentiment: {sentiment}")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'review': review_text,
            'sentiment': sentiment
        })
    }


_____________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________



**IAM Permissions Required**
EC2 Full Access (for instance management)
CloudWatch Logs (for logging)
Amazon Comprehend Access (for sentiment analysis)


**Output Verification**
Lambda execution via test events
Logs checked in CloudWatch
EC2 and EBS actions verified in AWS Console


**Key Learnings**
Serverless automation using AWS Lambda
Infrastructure management using Boto3
Event-driven architecture
AWS AI service integration (Comprehend)


**Author**

**Madhu Singh
Cloud & DevOps Engineer (Azure | AWS | Terraform)**


