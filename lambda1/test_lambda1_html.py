from lambda1_html import lambda_handler
import json
import boto3
from datetime import datetime
import requests_mock


def test_lambda_handler():
    s3 = boto3.client('s3')

    expected_body = 'Hello, world!'
    with requests_mock.Mocker() as m:
        m.get('https://casas.mitula.com.co/searchRE/'
              'nivel3-Chapinero/nivel2-Bogotá/nivel1-Cundinamarca/'
              'q-Bogotá-Chapinero',
              text=expected_body)

        event = {}
        context = {}
        response = lambda_handler(event, context)

        assert response['statusCode'] == 200
        assert response['body'] == json.dumps('Hello from lambda!!!')

        objects = s3.list_objects(Bucket='landing-casas-09')
        keys = [obj['Key'] for obj in objects['Contents']]
        assert str(datetime.today().strftime('%Y-%m-%d')) + '.html' in keys

        obj = s3.get_object(Bucket='landing-casas-09',
                            Key=str(datetime.today().strftime('%Y-%m-%d')) + '.html')
        assert obj['Body'].read().decode('utf-8') == expected_body
