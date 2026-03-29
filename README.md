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

```

Screenshot:

First EC2 machine created with tag Auto Stat 
<img width="940" height="461" alt="image" src="https://github.com/user-attachments/assets/508ea41c-d8cc-4359-9e16-964d48ab2899" />

Second EC2 machine created with tag Auto Stop
<img width="940" height="478" alt="image" src="https://github.com/user-attachments/assets/097ce65f-b9b4-4458-81cd-9323c4e3047c" />

 
Current status:
<img width="940" height="162" alt="image" src="https://github.com/user-attachments/assets/9a866572-3ed7-4d95-8b86-94ae9809e1a9" />

 

Post lambda function creates with full ec2 access using boto3 in lambda function.
<img width="940" height="450" alt="image" src="https://github.com/user-attachments/assets/8e2a1281-fc3c-4b5c-8792-6af1235bcebd" />
<img width="940" height="155" alt="image" src="https://github.com/user-attachments/assets/74d0f519-7fa6-4b76-9fc2-9c8ac5e4ccee" />


 

 
Post tag EC2 Status:
<img width="940" height="159" alt="image" src="https://github.com/user-attachments/assets/1dbeb5eb-9868-459b-990b-4937506c6a3f" />

 


____________________________________________________________________________________________
____________________________________________________________________________________________


Assignment 4: Automatic EBS Snapshot & Cleanup
 Objective

Create EBS snapshots and delete old snapshots automatically.

 Lambda Function Code:
 
```python
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

```

Screenshot:

Under EBS 3 Volumes and 2 snapshots present, post creating lambda function to detect EBS snapshots and perform cleanup

<img width="940" height="356" alt="image" src="https://github.com/user-attachments/assets/14e4538e-c69c-4f79-92df-1c3f563e5f7b" />


 
Lambda Function:
<img width="940" height="378" alt="image" src="https://github.com/user-attachments/assets/bdfd87f8-0ead-44a4-afca-c4cd24a58453" />

<img width="940" height="531" alt="image" src="https://github.com/user-attachments/assets/8fbb1ac1-feb1-47c9-8421-306fb7548063" />

Snapshots deleted: 
<img width="940" height="431" alt="image" src="https://github.com/user-attachments/assets/b8d019f8-2477-4dbc-8276-6cb1021af208" />

 


_______________________________________________________________________________________________
_______________________________________________________________________________________________


Assignment 5: Auto-Tagging EC2 Instances
 Objective

Automatically tag EC2 instances at launch.

Lambda Function Code

```python

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
```

New EC2 Instances created: 
<img width="940" height="185" alt="image" src="https://github.com/user-attachments/assets/ebcbada7-1171-4e2a-9227-310b5c2f80c2" />

Lambda Function: 
<img width="940" height="475" alt="image" src="https://github.com/user-attachments/assets/63bc1a14-ae60-4df2-8194-8c589bea6acc" />

<img width="940" height="298" alt="image" src="https://github.com/user-attachments/assets/c27d8d5d-6149-4d10-a33b-9ceca529e65c" />




_____________________________________________________________________________________________________
_____________________________________________________________________________________________________



Assignment 8: Sentiment Analysis using Amazon Comprehend
 Objective

Analyze sentiment of user reviews using AWS AI service.

 Service Used
Amazon Comprehend

 Lambda Function Code
 
```python

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

```


 IAM role created using AWS Lambda, Boto3, and Amazon Comprehend

 <img width="940" height="565" alt="image" src="https://github.com/user-attachments/assets/92e389b6-3c6e-43fa-a74a-3202edbc6f26" />

Test Results:
<img width="940" height="464" alt="image" src="https://github.com/user-attachments/assets/c7bd9983-23d1-4bf4-9d36-731f66674217" />


Here Sentiment of User Reviews Using AWS Lambda, Boto3, and Amazon Comprehend has been reviewd.


<img width="940" height="418" alt="image" src="https://github.com/user-attachments/assets/24f39b1c-4422-4a5f-b6d2-0a83fafe90da" />

<img width="940" height="395" alt="image" src="https://github.com/user-attachments/assets/52dce81e-720d-441b-ab6f-728b55ba685a" />




____________________________________________________________________________________________________________________
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


