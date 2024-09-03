import json
import boto3

def lambda_handler(event, context):
    # Extrair o CPF do header
    cpf = event['headers'].get('cpf')
    
    if not cpf:
        return {
            'statusCode': 400,
            'body': 'CPF não fornecido no header.'
        }

    # Conectar ao Cognito
    client = boto3.client('cognito-idp')

    user_pool_id = 'sa-east-1_Vk8Ngd5Iy'  # Substitua pelo ID do seu User Pool
    cpf_field = 'preferred_username'  # O campo customizado onde o CPF foi salvo no Cognito

    try:
        # Certifique-se de que o CPF está no formato correto
        cpf = cpf.strip()  # Remove espaços em branco
        if len(cpf) != 11 or not cpf.isdigit():
            return {
                'statusCode': 400,
                'body': 'CPF inválido. O CPF deve conter 11 dígitos numéricos.'
            }

        # Buscar usuário pelo CPF
        filter_expression = f'{cpf_field}="{cpf}"'
        response = client.list_users(
            UserPoolId=user_pool_id,
            Filter=filter_expression
        )
        
        # Verificar se o CPF está associado a algum usuário
        if response['Users']:
            return {
                'statusCode': 200,
                'body': 'CPF válido. Usuário encontrado.'
            }
        else:
            return {
                'statusCode': 404,
                'body': 'CPF inválido. Usuário não encontrado.'
            }

    except client.exceptions.InvalidParameterException as e:
        return {
            'statusCode': 400,
            'body': f'Erro nos parâmetros fornecidos: {str(e)}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Erro ao verificar o CPF: {str(e)}'
        }
