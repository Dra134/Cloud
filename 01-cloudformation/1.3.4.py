import boto3
import json

# Define the default friendly name for the S3 bucket
friendly_name = "my-s3-bucket"

# Read the target deployment regions from a configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Create a CloudFormation client
cfn = boto3.client('cloudformation')

# Define a function to find the existing stacks in all the regions
def find_stacks():
    # Create an empty list to store the stack names
    stacks = []
    
    # Loop through the regions to find the stack in each region
    for region in config['regions']:
        # Set the unique stack name based on the current region
        stack_name = "s3-bucket-" + region
        
        # Try to describe the stack in the current region
        try:
            cfn.describe_stacks(StackName=stack_name)
            # If the stack exists, add its name to the list of stacks
            stacks.append(stack_name)
        # If the stack does not exist, ignore the exception and move on to the next region
        except cfn.exceptions.StackDoesNotExist:
            pass
    # Return the list of stack names
    return stacks

# Define a function to delete the stacks
def delete_stacks(stacks):
    # Loop through the stack names
    for stack_name in stacks:
        # Delete the stack
        cfn.delete_stack(StackName=stack_name)
        # Wait until the stack deletion is complete
        cfn.get_waiter('stack_delete_complete').wait(StackName=stack_name)

def create_update_stacks():
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

# Find existing stacks
stacks = find_stacks()

# Delete existing stacks
if len(stacks) > 0:
    delete_stacks(stacks)

# Create/Update stacks
create_update_stacks()

# Check if the S3 buckets have been deleted
s3 = boto3.client('s3')
buckets = s3.list_buckets()
for bucket in buckets['Buckets']:
    if friendly_name in bucket['Name']:
        print(f"Error: S3 bucket '{bucket['Name']}' still exists.")

print("All S3 buckets have been successfully deleted.")
