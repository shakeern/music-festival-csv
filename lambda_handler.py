import boto3
import csv
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


#AWS Clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')

DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    try:
        #get s3 bucket
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']

        logger.info(f'Processing file {file_key} from bucket {bucket_name}')


        download_path = f"/tmp/{file_key}"
        s3_client.download_file(bucket_name, file_key, download_path)

        #parse csv
        performances = parse_csv(download_path)

        #insert into DynamoDB
        insert_to_dynamodb(performances)

        #sns to email
        send_sns_notification(f"Successfully processes file: {file_key}", success = True)

        return {"statusCode": 200, "body": "File processed successfully"}
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        send_sns_notification(f"Error processing file: {str(e)}", success=False)
        return {"statusCode":500, "body": "Error processing file"}
    
def parse_csv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                "Performer" : row["Performer"],
                "Stage": row["Stage"],
                "Start": row["Start"],
                "End": row["End"],
                "Date" : row["Date"]
            })
    logger.info(f"Parsed {len(data)} rows")
    return data
def insert_to_dynamodb(data):
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    with table.batch_writer() as batch:
        for item in data:
            try:
                batch.put_item(
                    Item={
                        "Performer": item["Performer"],
                        "Stage": item["Stage"],
                        "Start": item["Start"],
                        "End": item["End"],
                        "Date": item["Date"]
                    }
                )
            except Exception as e:
                logger.error(f"Error inserting item {item}: {e}")
    logger.info(f"Inserted {len(data)} records into DynamoDB")


def send_sns_notification(message, success):
    subject = "CSV Processing Success" if success else "CSV Processing Failed"
    sns_client.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject=subject)
    logger.info(f"Notification sent: {subject}")