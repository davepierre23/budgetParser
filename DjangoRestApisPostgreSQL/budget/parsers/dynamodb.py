import boto3

# Replace with your AWS credentials and region
aws_access_key_id = 'your_access_key_id'
aws_secret_access_key = 'your_secret_access_key'
aws_region = 'your_aws_region'

# Initialize a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Define the table name
table_name = 'YourTableName'

# Sample data to be added
data = [
    {
        'Category': 'Groceries',
        'Date': '2023-07-09',
        'Amount': -8.84
    },
    {
        'Category': 'Dining Out',
        'Date': '2023-07-08',
        'Amount': -72.09
    },
    # Add more data as needed
]

# Add data to the DynamoDB table
for item in data:
    response = dynamodb.put_item(
        TableName=table_name,
        Item={
            'Category': {'S': item['Category']},
            'Date': {'S': item['Date']},
            'Amount': {'N': str(item['Amount'])}
        }
    )

    print(f"Added item to DynamoDB: {item}")

print("Data has been added to the DynamoDB table.")
