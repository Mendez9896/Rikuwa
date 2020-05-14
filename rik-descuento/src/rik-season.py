import os
import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
import decimal
from botocore.exceptions import ClientError




def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    pedidos= dynamodb.Table('fedex')
    cant = event["queryStringParameters"]["cant"]
    desc = int(cant)/100
    desc = Decimal(str(desc))
    try:
        
        update = pedidos.update_item(
            Key={
                'pk': "season-desc",
                'sk': "season-desc"
            },
            UpdateExpression="set Descuento = :r",
            ExpressionAttributeValues={
                ':r': desc
            },
            ReturnValues="UPDATED_NEW"
        )
        response = "Actualizacion correcta"
    except ClientError as e:
        response = "No se pudo actualizar"
    
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }