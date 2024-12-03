# Full Stack Engineering Challenge

## Overview:
This project implement a secure, scalable, and cost-effecient system using AWS services such as Lambda, S3, DynamoDB, and SNS. When a music festival lineup csv file is uploaded to a s3 bucket, and lambda function is triggered, which
parses the csv and adds it to a DynamoDB database. A SNS notification is sent as an Email.

## DynamoDB Design Schema:
The DynamoDB is optimized for effecient querying based on Performer, Stage, and Time. 
### Partition Key: Performer
This partition key ensures data for each performer is stored together, allowing effecient retreival of all performances by a specific performer.
### Sort key: Start 
The sort key organizes performances chronologically by start time for each performer. This structure supports efficient range queries for performances occurring within a given time frame.
### Global Secondary Index:
### Partition Key: Stage
The GSI partition key allows querying performances by stage, regardless of performer.
### Sort key: Date
The sort key in the GSI enables efficient ordering and retreival of performances based on their date on that stage.
Benefits of the Design
Efficient Performer-Based Queries: Fetching all performances for a performer or those within a specific time is optimized with the main table schema.
Flexible Stage-Based Queries: The GSI supports efficient queries to list all performances on a particular stage, sorted by their dates.
Query Flexibility: The table and GSI support all required queries:
Retrieve all performances by a specific performer, ordered by time.
List all performances on a stage, ordered by date.
Fetch details of a specific performance by stage and start time.


## Cost Analysis
File Size: Each 100 lines of CSV = ~5 KB.
Daily Records: 1,000, 10,000, and 100,000 records.
Storage Costs:
DynamoDB costs: $0.25/GB for storage
S3: 0.023/Gb 


For 1000 records (0.05 GB): (0.05 * 0.023) + (0.05 * 0.25) = $0.0125 per day
For 10000 records (0.5 GB): (0.5 * 0.023) + (0.5 * 0.25) = $0.1365 per day
For 100000 records (5 GB): (5 * 0.023) + (5 * 0.25) = $1.365 per day

## Scalability Analysis
1. S3 Lifecycle policies can be used to manage the data lifecycle and delete them when they are no longer needed.
2. On-Demand Capacity Mode for DynamoDB can automatically adjust its read nad write based on the demand. 


## Permissions and Security:
Lambda Permissions:
S3 Read-Only Access: Allows the Lambda function to read CSV files from the S3 bucket.
DynamoDB Access: Grants permissions to write and query the DynamoDB table.
SNS Publish Access: Enables the Lambda function to send notifications to an SNS topic.

IAM Principles
Least Privilege: All roles have minimal permissions to perform necessary actions, ensuring a secure setup.
Resource Policies: Access to the S3 bucket, DynamoDB table, and SNS topic is restricted to the Lambda execution role.

Shakeer Nawaz
s1nawaz@torontomu.ca
