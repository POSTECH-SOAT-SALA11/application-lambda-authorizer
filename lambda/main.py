import json
import boto3
from botocore.exceptions import ClientError

cognito_client = boto3.client('cognito-idp')

USER_POOL_ID = 'sa-east-1_GSR1Kl3jx'
APP_CLIENT_ID = '28qfrp9p1t9n5d27dr1o3i1e5e'

def lambda_handler(event, context):
    cpf = event['queryStringParameters'].get('cpf')

    if not cpf:
        return {
            'statusCode': 400,
            'body': json.dumps('CPF is required')
        }

    try:
        response = cognito_client.list_users(
            UserPoolId=USER_POOL_ID,
            Filter=f'custom:cpf="{cpf}"'
        )

        if len(response['Users']) == 0:
            return {
                'statusCode': 401,
                'body': json.dumps('User not found')
            }

        user = response['Users'][0]
        return {
            'statusCode': 200,
            'body': json.dumps(f'User authenticated: {user["Username"]}')
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error authenticating user: {str(e)}')
        }
