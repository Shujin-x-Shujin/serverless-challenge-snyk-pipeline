import json
import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr

db = boto3.resource('dynamodb')
table_name = 'loyalty-cards'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
def index(event, context):
    body = {
        'message' : 'Welcome Home !',
        'input': event
    }
    return {'statusCode': 200, 'body': json.dumps(body)}

def get_all_loyalty_cards(event: any, context: any):
    table = db.Table(table_name)
    cards = []

    response = table.scan()
    cards.extend(response.get('Items'))

    return {
        'statusCode': 200,
        'body': json.dumps(cards)
    }
    
           

def get_loyalty_card_by_key(event: any, context: any):
    logger.info(json.dumps(event))
    id_value = event['queryStringParameters'].get('id')

    if id_value is None:
        return {
            'statusCode': 404,
            'body': json.dumps('ID not provided')
        }
    table = db.Table(table_name)
    card = []
    response = table.query(
        KeyConditionExpression=Key('id').eq(id_value)
    )
    items = response.get('Items')
    if items is not None:
        card.extend(items)

    return {
        'statusCode': 200,
        'body': json.dumps(card)
    }
def create_loyalty_card(event: any, context: any):
    logger.info(json.dumps(event))
    data_to_insert =  json.loads(event['body'])
    table = db.Table(table_name)
    response = table.put_item(Item=data_to_insert)

    print(f'Item inserted successfully: {response}')
    print(data_to_insert)

    return {
        'statusCode': 201,
        'body': json.dumps('Item inserted successfully!')
    }
    