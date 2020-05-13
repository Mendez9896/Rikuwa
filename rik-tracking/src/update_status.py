import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

status_list = ['registering', 'checkout', 'packaging', 'embarking', 'enroute', 'arrival', 'delivery', 'finish']

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('fedex')
    package_id = event['queryStringParameters']['package_id']
    
    query = table.query(
        KeyConditionExpression=Key('pk').eq(package_id) & Key('sk').eq(package_id)
    )
    
    if 'Items' not in query or len(query['Items']) <= 0: 
        return {
            'statusCode': 404,
            'body': json.dumps(f"El paquete '{package_id}' no existe")
        }
    
    package = query['Items'][0]
    package_status = package['package_status']
    
    if package_status not in status_list:
        return {
            'statusCode': 500,
            'body': json.dumps(f"El paquete '{package_id}' tiene un estado invalido")
        }
        
    if package_status == status_list[-1]:
        return {
            'statusCode': 200,
            'body': json.dumps(package)
        }
    
    if package_status == 'enroute' and package['stop'] == 'true':
        new_status = 'embarking'
        stop = 'false'
    else:
        new_status = status_list[status_list.index(package_status)+1]
        stop = package['stop']
        
    update = table.update_item(
        Key={
            'pk': package_id,
            'sk': package_id
        },
        UpdateExpression="set package_status = :s, stop = :x",
        ExpressionAttributeValues={
            ':s': new_status,
            ':x': stop
        },
        ReturnValues="UPDATED_NEW"
    )
    package['package_status'] = new_status
    package['stop'] = stop
    
    return {
            'statusCode': 200,
            'body': json.dumps(package)
        }
    
    
    