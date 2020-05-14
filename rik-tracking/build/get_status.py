import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

status_list = ['registering', 'checkout', 'packaging', 'embarking', 'enroute', 'arrival', 'delivery']

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('fedex')
    package_id = event['queryStringParameters']['package_id']
    user_id = event['queryStringParameters']['user_id']
    
    query = table.query(
        KeyConditionExpression=Key('pk').eq(package_id)&Key('sk').eq(user_id)
    )
    
    if 'Items' not in query or len(query['Items']) <= 0: 
        return {
            'statusCode': 404,
            'body': json.dumps(f"El paquete '{package_id}' no existe")
        }
    
    package = query['Items'][0]
    
    if package['Status package'] not in status_list:
        return {
            'statusCode': 500,
            'body': json.dumps(f"El paquete '{package_id}' tiene un estado invalido")
        }
    
    return {
            'statusCode': 200,
            'body': json.dumps(package)
    }