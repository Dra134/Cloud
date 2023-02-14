import boto3
import json

# Define the default friendly name for the S3 bucket
friendly_name = "my-s3-bucket"

# Read the target deployment regions from a configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Create a CloudFormation client
cfn = boto3.client('cloudformation')

# Loop through the regions to deploy the S3 bucket in each region
for region in config['regions']:
    # Set the unique bucket name based on the current region and friendly name
    bucket_name = "current-" + region + "-" + friendly_name

    # Check if the stack already exists in the current region
    try:
        cfn.describe_stacks(StackName="s3-bucket-" + region)
    except cfn.exceptions.StackDoesNotExist:
        # Deploy the CloudFormation stack in the current region
        cfn.create_stack(
            StackName="s3-bucket-" + region,
            TemplateBody=open("s3-bucket-template.yaml").read(),
            Parameters=[
                {
                    "ParameterKey": "BucketName",
                    "ParameterValue": bucket_name
                }
            ],
            RegionName=region
        )
    else:
        # Update the CloudFormation stack in the current region
        cfn.update_stack(
            StackName="s3-bucket-" + region,
            TemplateBody=open("s3-bucket-template.yaml").read(),
            Parameters=[
                {
                    "ParameterKey": "BucketName",
                    "ParameterValue": bucket_name
                }
            ],
            RegionName=region
        )
