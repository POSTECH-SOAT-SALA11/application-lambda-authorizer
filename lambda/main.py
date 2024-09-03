import json
import boto3

def lambda_handler(event, context):
    # Extrair o CPF do header
    cpf = event['headers'].get('cpf')
    
    if not cpf:
        return {
            'statusCode': 400,
            'body': json.dumps('CPF não fornecido no header.')
        }

    # Conectar ao Cognito
    client = boto3.client('cognito-idp')

    user_pool_id = 'sa-east-1_ycgIX6Are'  # Substitua pelo ID do seu User Pool
    cpf_field = 'custom:cpf'  # O campo customizado onde o CPF foi salvo no Cognito

    try:
        # Buscar usuário pelo CPF
        response = client.list_users(
            UserPoolId=user_pool_id,
            Filter=f'{cpf_field} = "{cpf}"'
        )
        
        # Verificar se o CPF está associado a algum usuário
        if response['Users']:
            return {
                'statusCode': 200,
                'body': json.dumps('CPF válido. Usuário encontrado.')
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('CPF inválido. Usuário não encontrado.')
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao verificar o CPF: {str(e)}')
        }
