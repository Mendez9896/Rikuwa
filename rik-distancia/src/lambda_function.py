#!/usr/bin/python3

import requests
import json
import boto3

def lambda_handler(event, context):
    
    #Obtener Origen y destino
    origin="La paz"
    destination="Madrid"
    final_distance=0
    api_table_name="api-cache-table"
    #Revisar si estan en la tabla api-cache-table
    dynamo = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    api_table = DB.Table(api_table_name)
    
    response_api_table = api_table.get_item(
            Key={
                'Origin': origin,
                'Destination': destination
            }
        ) 
    
    #Si estan, devolver Distance
    if 'Item' in response_api_table:
        check=response_api_table['Item']
        final_distance=int(json.dumps(check['Distance']))
        #print(":D")
        
    #En otro caso, utilizar la api
    else:
        response = requests.get('https://www.distance24.org/route.json?stops='+origin+'|'+destination)
        distance_api_object = json.loads(response.content)
        final_distance=int(json.dumps(distance_api_object['distance']))
        
        print(json.dumps(distance_api_object['travel']['general']['countries']))
        
    #Llenar la tabla api-cache-table con Origin, Destination y Distance y tambien Destination, Origin y Distance
        item=api_table.put_item(
                Item={
                    'Origin': origin,
                    'Destination': destination,
                    'Distance': final_distance
                }
            
            )
        item_reverse=api_table.put_item(
                Item={
                    'Origin': destination,
                    'Destination': origin,
                    'Distance': final_distance
                }
            
            )
            
    #print(distance_api_object['distances'])
    #Devolver la distancia final
    return {
        'statusCode': 200,
        'body': final_distance
    }
    
lambda_handler(None, None)