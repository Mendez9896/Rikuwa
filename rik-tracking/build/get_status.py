import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

status_list = ['registering', 'checkout', 'packaging', 'embarking', 'enroute', 'arrival', 'delivery', 'finish']

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('fedex')
    package_id = event['queryStringParameters']['package_id']
    query = table.query(
        KeyConditionExpression=Key('pk').eq(package_id)
    )
    
    if 'Items' not in query or len(query['Items']) <= 0: 
        return {
            'statusCode': 404,
            'body': json.dumps(f"El paquete '{package_id}' no existe")
        }
    
    package = query['Items'][0]
    
    if package['Statuspackage'] not in status_list:
        return {
            'statusCode': 500,
            'body': json.dumps(f"El paquete '{package_id}' tiene un estado invalido")
        }
    
    return {
            'statusCode': 200,
            'body': json.dumps(package['Statuspackage'])
    }