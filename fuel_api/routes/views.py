from django.http import JsonResponse
import pandas as pd
import requests
import logging
import json
import os
from django.shortcuts import render
import folium
import plotly.express as px

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# URL e API Key do OpenRouteService
MAPS_API_URL = "https://api.openrouteservice.org/v2/directions/driving-car"
API_KEY = '5b3ce3597851110001cf6248f6958d2a6a1749988544daf0569884f9'

# Variável global para armazenar os dados de combustível
fuel_data = None

def load_fuel_data():
    global fuel_data
    try:
        fuel_data = pd.read_csv('fuel_prices.csv').to_dict(orient='records')
        logging.info("Dados de combustível carregados com sucesso.")
    except FileNotFoundError:
        fuel_data = None
        logging.error("Arquivo 'fuel_prices.csv' não encontrado.")

load_fuel_data()

def calculate_total_cost(distance):
    range_per_tank = 500  # em milhas
    gallons_needed = distance / 10  # supondo 10 milhas por galão
    fuel_prices = [float(stop['Retail Price']) for stop in fuel_data]

    if not fuel_prices:
        logging.error("Nenhum preço de combustível disponível.")
        return 0
    
    cost_total = gallons_needed * (sum(fuel_prices) / len(fuel_prices))
    return cost_total

def find_fuel_stops(distance):
    range_per_tank = 500  # em milhas
    fuel_stops = []
    total_distance_covered = 0

    for stop in fuel_data:
        if total_distance_covered + range_per_tank <= distance:
            fuel_stops.append({
                'Truckstop_Name': stop['Truckstop Name'],
                'Address': stop['Address'],
                'City': stop['City'],
                'State': stop['State'],
                'Retail_Price': stop['Retail Price']
            })
            total_distance_covered += range_per_tank

    return fuel_stops

def get_route(request):
    logging.info("Iniciando o processamento da rota")
    
    start = request.GET.get('start')
    end = request.GET.get('end')

    if not start or not end:
        logging.error("Coordenadas de início e fim são obrigatórias.")
        return JsonResponse({"error": "Coordenadas de início e fim são obrigatórias."}, status=400)

    try:
        start_coords = [float(coord) for coord in start.split(',')]
        end_coords = [float(coord) for coord in end.split(',')]
        logging.info(f"Coordenadas de início: {start_coords}, Coordenadas de fim: {end_coords}")
    except ValueError:
        logging.error("Coordenadas inválidas. Use o formato 'longitude,latitude'.")
        return JsonResponse({"error": "Coordenadas inválidas. Use o formato 'longitude,latitude'."}, status=400)

    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }

    data = {
        "coordinates": [start_coords, end_coords],
        "profile": "driving-car",
        "format": "geojson"
    }

    logging.info(f"Dados da requisição: {data}")
    response = requests.post(MAPS_API_URL, json=data, headers=headers)

    logging.info(f"Resposta da API: {response.status_code} - {response.json()}")

    if response.status_code != 200:
        logging.error(f"Erro ao obter rota: {response.status_code}, {response.text}")
        return JsonResponse({"error": f"Erro ao obter rota: {response.status_code}, {response.text}"}, status=500)

    route_data = response.json()
    logging.info("Resposta da API (formatada): %s", json.dumps(route_data, indent=2))
    
    if 'features' not in route_data or not route_data['features']:
        logging.error("A resposta da API não contém recursos.")
        return JsonResponse({"error": "A resposta da API não contém recursos.", "response": route_data}, status=500)

    try:
        segments = route_data['features'][0]['properties']['segments']
        total_distance_miles = sum(segment['distance'] for segment in segments) / 1609.34
        total_amount = sum(segment['amount'] for segment in segments)
    except (IndexError, KeyError) as e:
        logging.error(f"Erro ao processar os dados da rota: {str(e)}")
        return JsonResponse({"error": f"Erro ao processar os dados da rota: {str(e)}"}, status=500)

    cost_total = calculate_total_cost(total_distance_miles)
    fuel_stops = find_fuel_stops(total_distance_miles)

    # Criar o mapa com Folium
    coords = [(point[1], point[0]) for point in route_data['features'][0]['geometry']['coordinates']]
    latitudes, longitudes = zip(*coords)

    # Verificar e criar o diretório se não existir
    map_dir = os.path.join('static', 'maps')
    if not os.path.exists(map_dir):
        os.makedirs(map_dir)

    # Criar o mapa
    m = folium.Map(location=[(start_coords[1] + end_coords[1]) / 2, (start_coords[0] + end_coords[0]) / 2], zoom_start=6)
    folium.Marker(location=start_coords[::-1], popup='Início', icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=end_coords[::-1], popup='Fim', icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine(locations=[(lat, lon) for lon, lat in coords], color='blue').add_to(m)

    # Salvar o mapa em um arquivo HTML
    map_file = os.path.join(map_dir, 'map.html')
    m.save(map_file)
    logging.info("Salvando o mapa em %s", map_file)

    # Retornar a resposta JSON
    return JsonResponse({
        'route_distance': total_distance_miles,
        'total_amount': total_amount,
        'fuel_stops': fuel_stops,
        'total_cost': cost_total,
    })

def home(request):
    return render(request, 'home.html')

def route_view(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    if start and end:
        response = get_route(request)
        if isinstance(response, JsonResponse):
            data = response.json()
            return render(request, 'home.html', {
                'route_distance': data['route_distance'],
                'total_cost': data['total_cost'],
                'fuel_stops': data['fuel_stops'],
            })

    return render(request, 'home.html')
