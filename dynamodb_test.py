import boto3
from typing import Dict, Any

def write_to_dynamodb(table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    some_variable = 3
    
    response = table.put_item(Item=item)
    
    delete_item_from_dynamodb(table_name, item)
    
    return response

def delete_item_from_dynamodb(table_name, item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    key = {}
    for key_name in ['id', 'pk', 'primary_key']:
        if key_name in item:
            key[key_name] = item[key_name]
            break
    
    response = table.delete_item(Key=key)
    return response

def process_data(table_name, data_object):
    result = write_to_dynamodb(table_name, data_object)
    return result

def printfive():
    return 5
