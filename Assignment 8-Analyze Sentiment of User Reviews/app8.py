import json
import boto3

# Initialize Comprehend client
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    
    # 1. Extract review text from event
    review_text = event.get('review', '')
    
    if not review_text:
        return {
            'statusCode': 400,
            'body': json.dumps('No review text provided')
        }
    
    # 2. Call Amazon Comprehend
    response = comprehend.detect_sentiment(
        Text=review_text,
        LanguageCode='en'
    )
    
    sentiment = response['Sentiment']
    
    # 3. Log the result
    print(f"Review: {review_text}")
    print(f"Sentiment: {sentiment}")
    
    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'review': review_text,
            'sentiment': sentiment
        })
    }