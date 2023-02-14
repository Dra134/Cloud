import boto3
import json

# Define the default friendly name for the S3 bucket
friendly_name = "my-s3-bucket"

# Read the target deployment regions from a configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Create a CloudFormation client
cfn = boto3.client('cloudformation')

# Create a S3 client
s3 = boto3.client('s3')

# Loop through the regions to deploy or delete the S3 bucket in each region
for region in config['regions']:
    # Set the unique bucket name based on the current region and friendly name
    bucket_name = "current-" + region + "-" + friendly_name

    # Check if the stack already exists in the current region
    try:
        cfn.describe_stacks(StackName="s3-bucket-" + region)
    except cfn.exceptions.StackDoesNotExist:
        # If the stack does not exist, delete the S3 bucket if it exists
        try:
            s3.head_bucket(Bucket=bucket_name)
        except s3.exceptions.NoSuchBucket:
            pass
        else:
            # Delete all objects in the S3 bucket
            for obj in s3.list_objects(Bucket=bucket_name)['Contents']:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])

            # Delete the S3 bucket
            s3.delete_bucket(Bucket=bucket_name)
    else:
        # If the stack exists, delete the stack
        cfn.delete_stack(StackName="s3-bucket-" + region)
