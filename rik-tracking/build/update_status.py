import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

status_list = ['registering', 'checkout', 'packaging', 'embarking', 'enroute', 'arrival', 'delivery', 'finish']

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    sns = boto3.client('sns')
    table = dynamodb.Table('fedex')
    disttable = dynamodb.Table('api-cache-table')
    
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
    package_status = package['Statuspackage']
    
    if package_status not in status_list:
        return {
            'statusCode': 500,
            'body': json.dumps(f"El paquete '{package_id}' tiene un estado invalido")
        }
        
    if package_status == status_list[-1]:
        return {
            'statusCode': 200,
            'body': json.dumps(package_status)
        }
        
    if package_status == status_list[0]:
        topic = sns.create_topic(
            Name= f"{package_id}-topic"
        )
        subs_arn = sns.subscribe(
            TopicArn = topic['TopicArn'],
            Protocol= 'Email',
            Endpoint= package['email'],
            ReturnSubscriptionArn=True
        )
        table.update_item(
            Key={
                'pk': package_id,
                'sk': package['sk']
            },
            UpdateExpression="set topic_arn = :a",
            ExpressionAttributeValues={
                ':a': topic['TopicArn']
            },
            ReturnValues="UPDATED_NEW"
        )
        
        query = disttable.query(
            KeyConditionExpression=Key('origin').eq(package['Origin'])&Key('destination').eq(package['Destination'])
        )
        
        if len(query['Items']) <= 0:
            stop = 'false'
        else:
            dist = query['Items'][0]
            if dist['stop'] == '':
                stop = 'false'
            else:
                stop = 'true'
                
        package['stop'] = stop
        
        
        
        
    
    if package_status == 'enroute' and package['stop'] == 'true':
        new_status = 'embarking'
        stop = 'false'
    else:
        new_status = status_list[status_list.index(package_status)+1]
        stop = package['stop']
        
    update = table.update_item(
        Key={
            'pk': package_id,
            'sk': package['sk']
        },
        UpdateExpression="set Statuspackage = :s, stop = :x",
        ExpressionAttributeValues={
            ':s': new_status,
            ':x': stop
        },
        ReturnValues="UPDATED_NEW"
    )
    
    
    if package_status == status_list[0]:
        topic_arn = topic['TopicArn']
    else:
        topic_arn = package['topic_arn']
        
    sns.publish(
        TopicArn=topic_arn,
        Message=f"Su paquete con codigo {package_id} se actualiza al estado: '{new_status}'",
        Subject='Fedex'
    )
    
    
    package['package_status'] = new_status
    package['stop'] = stop
    package['topic_arn'] = topic_arn
    
    return {
            'statusCode': 200,
            'body': json.dumps(new_status)
        }
    
    
    