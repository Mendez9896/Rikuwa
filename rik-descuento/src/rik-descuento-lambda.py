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
    distancias = dynamodb.Table('api-cache-table')
    print(event)
    idPack = event["queryStringParameters"]["id"]
    descuento = 0
    items = pedidos.query( 
        KeyConditionExpression= Key('pk').eq(idPack) 
    )
    paquete = items["Items"][0]
    
    distItems = distancias.query(
        KeyConditionExpression= Key('Origen').eq(paquete["Origen"]) & Key('Destino').eq(paquete["Destino"])    
    )
    dist = distItems["Items"][0]
    
    usuarioItem = pedidos.query(
        KeyConditionExpression= Key('pk').eq(paquete['sk']) & Key('sk').eq(paquete['sk'])
    )
    
    usuario = usuarioItem["Items"][0]
    
    descItem = pedidos.query(
        KeyConditionExpression= Key('pk').eq("season-desc") & Key('sk').eq("season-desc")
    )
    
    seasonDesc = descItem["Items"][0]
    
    if usuario["count"] > 9:
        descuento = Decimal(str(0.15))
    elif usuario["count"] > 4:
        descuento= Decimal(str(0.1))
    
    descuento = descuento + seasonDesc["Descuento"]
    
    precio =( (dist["Distance"]/100) + Decimal(str(max(paquete["Package weight"]*Decimal(str(0.5)),paquete["Package dimension"]/100)))) * Decimal(str((1-descuento)))
    precio = Decimal(str(precio))
    try:
        
        update = pedidos.update_item(
            Key={
                'pk': idPack,
                'sk': paquete['sk']
            },
            UpdateExpression="set Price = :r",
            ExpressionAttributeValues={
                ':r': precio
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