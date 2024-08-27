import json

def handler(event, context):
    """
    Lambda function handler that returns a simple 'Hello, World!' message.

    Parameters:
    event (dict): AWS Lambda uses this parameter to pass in event data to the handler.
    context (object): AWS Lambda uses this parameter to provide runtime information to your handler.

    Returns:
    dict: A dictionary with a status code and a body containing the 'Hello, World!' message.
    """
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello, World!"aaaa
        })
    }

    return response
