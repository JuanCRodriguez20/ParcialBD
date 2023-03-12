import boto3
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='landing-casas-09', Key=str(datetime.today().strftime('%Y-%m-%d'))+'.html')
    body = obj['Body'].read()
    
    soup = BeautifulSoup(body, 'html.parser')

    listings = soup.find_all('div', {'class': 'listing listing-card'})
    
    csv_data = "FechaDescarga, Barrio, Valor, NumHabitaciones, NumBanos, mts2\n"
    print(listings.__len__())
    
    for listing in listings:
        fecha_descarga = datetime.today().strftime('%Y-%m-%d')
        try:
            barrio = listing.find('div', {'class': 'listing-card__location'}).text.strip()
        except:
            barrio = None
        
        try:
            valor = listing.find('div', {'class': 'price'}).text.strip()
        except:
            valor = float('inf')
        try:
            num_habitaciones = listing.find('span', {'content': '3'}).text.strip()
        except:
            num_habitaciones = float('inf')
        try:
            num_banos = listing.find('span', {'content': '2'}).text.strip()
        except:
            num_banos = float('inf')
        try:
            mts2 = listing.find('div', {'class': 'card-icon__area'}).find_next_sibling('span').text.strip()
        except:
            mts2 = float('inf')
            
        print(f'fecha Descarga: {fecha_descarga},Barrio: {barrio}, Valor: {valor}, NumHabitaciones: {num_habitaciones}, NumBanos: {num_banos}, mts2: {mts2}')
    
        csv_data += f"{fecha_descarga}, {barrio}, {valor}, {num_habitaciones}, {num_banos}, {mts2}\n"
            
    s3.put_object(Body=csv_data.encode(), Bucket='casas-final-09', Key=str(datetime.today().strftime('%Y-%m-%d'))+'.csv')

    return {
        'statusCode': 200,
        'body': 'Archivo CSV generado con éxito.'
    }
