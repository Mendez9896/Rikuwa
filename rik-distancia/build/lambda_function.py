#!/usr/bin/python3

import requests
import json
import boto3

def lambda_handler(event, context):
    
    origin=event['Origin']
    destination=event['Destination']
    final_distance=0
    api_table_name="api-cache-table"
    stop=""
    dynamo = boto3.client('dynamodb')
    DB = boto3.resource('dynamodb')
    api_table = DB.Table(api_table_name)
    
    response_api_table = api_table.get_item(
            Key={
                'Origin': origin,
                'Destination': destination
            }
        ) 
    
    if 'Item' in response_api_table:
        check=response_api_table['Item']
        final_distance=int(check['Distance'])
    else:
        response = requests.get('https://www.distance24.org/route.json?stops='+origin+'|'+destination)
        distance_api_object = json.loads(response.content)
        final_distance=int(json.dumps(distance_api_object['distance']))
        value=json.dumps(distance_api_object['travel']['general']['countries'])
        if "both" in value:
            stop="none"
        elif "Europe" in value:
            stop="winchester"
        elif "America" in value:
            stop="Miami"
        elif "Asia" in value:
            stop="Hong Kong"
        elif "Africa" in value:
            stop="Hong Kong"
        else:
            stop="Los Angeles"
        item=api_table.put_item(
                Item={
                    'Origin': origin,
                    'Destination': destination,
                    'Distance': final_distance,
                    'Stop': stop
                }
            
            )
        item_reverse=api_table.put_item(
                Item={
                    'Origin': destination,
                    'Destination': origin,
                    'Distance': final_distance,
                    'Stop': stop
                }
            
            )
    return {
        'statusCode': 200,
        'body': final_distance
    }