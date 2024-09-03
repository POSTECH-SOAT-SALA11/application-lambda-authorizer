import json
import boto3

def lambda_handler(event, context):

    cpf = event['headers'].get('cpf')
    
    if not cpf:
        return generate_policy("user", "Deny", event['methodArn'], "CPF não fornecido no header.")

    client = boto3.client('cognito-idp')

    user_pool_id = 'sa-east-1_B3wPiop9z'  
    cpf_field = 'preferred_username'

    try:
        cpf = cpf.strip()
        if len(cpf) != 11 or not cpf.isdigit():
            return generate_policy("user", "Deny", event['methodArn'], "CPF inválido. O CPF deve conter 11 dígitos numéricos.")

        filter_expression = f'{cpf_field}="{cpf}"'
        response = client.list_users(
            UserPoolId=user_pool_id,
            Filter=filter_expression
        )
        
        if response['Users']:
            return generate_policy("user", "Allow", event['methodArn'], "CPF válido. Usuário encontrado.")
        else:
            return generate_policy("user", "Deny", event['methodArn'], "CPF inválido. Usuário não encontrado.")

    except client.exceptions.InvalidParameterException as e:
        return generate_policy("user", "Deny", event['methodArn'], f'Erro nos parâmetros fornecidos: {str(e)}')
    except Exception as e:
        return generate_policy("user", "Deny", event['methodArn'], f'Erro ao verificar o CPF: {str(e)}')


def generate_policy(principal_id, effect, resource, message):
    """Helper function to generate an IAM policy"""
    auth_response = {}
    
    auth_response['principalId'] = principal_id

    if effect and resource:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
        auth_response['policyDocument'] = policy_document
    
    auth_response['context'] = {
        'message': message
    }
    
    return auth_response
