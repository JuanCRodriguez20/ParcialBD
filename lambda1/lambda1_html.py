import json
import boto3
from datetime import datetime
import requests


def lambda_handler(event, context):
    url = ("https://casas.mitula.com.co/searchRE/"
           "nivel3-Chapinero/nivel2-Bogotá/nivel1-Cundinamarca/"
           "q-Bogotá-Chapinero")
    body = requests.get(url)

    s3 = boto3.client('s3')
    s3.put_object(Body=body.content,
                  Bucket='landing-casas-09',
                  Key=str(datetime.today().strftime('%Y-%m-%d')) + '.html')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from lambda!!!')
    }
