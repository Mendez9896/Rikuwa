import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def handler(event, context):
    count= event['count']
    curstomer = event['curstomer']
    date = event['date']
    destination = event['destination']
    dimension= event['dimension']
    origin= event['origin']
    pk= event['curstomer']
    sk= event['sk']
    typeB = event['typeB']
    weight = event['weight']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('fedex')
    response2 = table.put_item(
        Item={
            "count": count,
            "curstomer": curstomer,
            "date": date,
            "destination": destination,
            "dimension": dimension,
            "origin": origin,
            "pk": curstomer,
            "sk": sk,
            "type": type,
            "weight": weight
        }    
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response2),
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
