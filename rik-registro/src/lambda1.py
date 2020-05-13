import os
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import uuid

def handler(event, context):
    idp1 = uuid.uuid1()
    idp = "pkg-" + str(idp1)
    pk = idp
    sk= "user-" + event['customer']
    
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
    
    response = table.scan()
    lst = []
    for i in response['Items']:
        lst.append(i['sk'])
    
    count=lst.count(sk)+1  
    
    
    response2 = table.put_item(
        Item={
            "pk": pk,
            "sk": sk,
            "Date": date,
            "Count": count,
            "Destination": destination,
            "Package dimension": dimension,
            "Origin": origin,
            "Package type": typeB,
            "Package weight": weight,
            "email": mail,
            "Status package": status,
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