from moto import mock_s3
from bs4 import BeautifulSoup
from datetime import datetime
from lambda2_data import lambda_handler
import boto3


@mock_s3
def test_lambda_handler():
    s3 = boto3.resource('s3', region_name='us-east-1')
    s3.create_bucket(Bucket='landing-casas-09')
    s3.create_bucket(Bucket='casas-final-09')

    test_html = """
        <html>
            <body>
                <div class="listing listing-card">
                    <div class="listing-card__location">Barrio 1</div>
                    <div class="price">$200,000</div>
                    <span content="3">3</span>
                    <span content="2">2</span>
                    <div class="card-icon__area"><span>100</span> mts2</div>
                </div>
                <div class="listing listing-card">
                    <div class="listing-card__location">Barrio 2</div>
                    <div class="price">$300,000</div>
                    <span content="4">4</span>
                    <span content="3">3</span>
                    <div class="card-icon__area"><span>200</span> mts2</div>
                </div>
            </body>
        </html>
    """

    test_date = datetime.today().strftime('%Y-%m-%d')
    test_key = f'{test_date}.html'

    s3.Object('landing-casas-09', test_key).put(Body=test_html)

    response = lambda_handler(None, None)

    test_csv_key = f'{test_date}.csv'

    assert s3.Bucket('casas-final-09').Object(test_csv_key).get()['Body'].read().decode() == f"FechaDescarga, Barrio, Valor, NumHabitaciones, NumBanos, mts2\n{test_date}, Barrio 1, $200,000, 3, 2, inf\n{test_date}, Barrio 2, $300,000, 3, inf, inf\n"
    assert response['statusCode'] == 200
    assert response['body'] == 'Archivo CSV generado con éxito.'


def test_lambda_handler_s3():
    s3 = boto3.client('s3')
    date = datetime.today().strftime('%Y-%m-%d')
    key = f'{str(date)}.html'
    obj = s3.get_object(Bucket='landing-casas-09', Key=key)
    body = obj['Body'].read()
    assert body is not None


def test_lambda_handler_soup():
    s3 = boto3.client('s3')
    date = datetime.today().strftime('%Y-%m-%d')
    key = f'{str(date)}.html'
    obj = s3.get_object(Bucket='landing-casas-09', Key=key)
    body = obj['Body'].read()
    soup = BeautifulSoup(body, 'html.parser')
    assert soup is not None
