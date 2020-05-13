import os
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import uuid

def handler(event, context):
    idp1 = uuid.uuid1()
    idp = str(idp1)
    pk = idp
    sk= idp
    package_id = idp
    count = 5
    customer = event['customer']
    date1 = datetime.date.today()
    date = date1.strftime('%m/%d/%Y')
    destination = event['destination']
    dimension1 = event['dimension']
    dimension= int(dimension1)
    origin= event['origin']
    typeB = event['typeB']
    weight1 = event['weight']
    weight = int(weight1)
    mail = event['mail']
    status = "registering"
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('fedex')
    
    object_key = event['customer']
    response = table.query(
        KeyConditionExpression=Key('curstomer').begins_with(customer)
    )
    l = len(response['Items'])
    
    
    response2 = table.put_item(
        Item={
            "pk": pk,
            "sk": sk,
            "date": date,
            "count": count,
            "curstomer": customer,
            "destination": destination,
            "dimension": dimension,
            "origin": origin,
            "type": typeB,
            "weight": weight,
            "mail": mail,
            "status": status,
            "package_id": package_id
        }    
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps(response2),
        "headers": {
            'Content-Type': 'application/json', 
            'Access-Control-Allow-Headers': 'x-requested-with',
            "Access-Control-Allow-Origin" : "*", 
            "Access-Control-Allow-Credentials" : 'true'
        }
    }