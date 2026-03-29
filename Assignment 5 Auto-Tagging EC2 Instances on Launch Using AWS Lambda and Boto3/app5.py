import boto3
from datetime import datetime
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    # Extract instance ID from the event
    instance_id = event['detail']['instance-id']
    launch_date = datetime.utcnow().strftime('%Y-%m-%d')
    # Add tags to the instance
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
        'body': f'Tags successfully added to {instance_id}'
    }