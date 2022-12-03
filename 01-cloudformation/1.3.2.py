import boto3

client = boto3.resource('cloudformation')

response = client.create_stack(
    StackName='sample stack',
    TemplateBody='string',
    TemplateURL='string',
    Parameters=[
        {
            'ParameterKey': 'string',
            'ParameterValue': 'string',
            'UsePreviousValue': True|False,
            'ResolvedValue': 'string'
        },
    ],
    DisableRollback=True|False,
    RollbackConfiguration={
        'RollbackTriggers': [
            {
                'Arn': 'string',
                'Type': 'string'
            },
        ],
        'MonitoringTimeInMinutes': 123
    },
    TimeoutInMinutes=123,
    NotificationARNs=[
        'string',
    ],
    Capabilities=[
        'CAPABILITY_IAM'|'CAPABILITY_NAMED_IAM'|'CAPABILITY_AUTO_EXPAND',
    ],
    ResourceTypes=[
        'string',
    ],
    RoleARN='string',
    OnFailure='DO_NOTHING'|'ROLLBACK'|'DELETE',
    StackPolicyBody='string',
    StackPolicyURL='string',
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ],
    ClientRequestToken='string',
    EnableTerminationProtection=True|False
)