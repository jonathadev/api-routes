from django.http import JsonResponse
import pandas as pd
import requests

# URL e API Key do OpenRouteService
MAPS_API_URL = "https://api.openrouteservice.org/v2/directions/driving-car"
API_KEY = '5b3ce3597851110001cf6248f6958d2a6a1749988544daf0569884f9'  # Insira sua chave da API do OpenRouteService aqui

# Variável global para armazenar os dados de combustível
fuel_data = None

def load_fuel_data():
    global fuel_data
    try:
        fuel_data = pd.read_csv('fuel_prices.csv').to_dict(orient='records')
    except FileNotFoundError:
        fuel_data = None

# Carregar os dados de combustível ao iniciar o módulo
load_fuel_data()

def calculate_route(request, start=None, end=None):
    if not start or not end:
        return JsonResponse({"error": "Please provide both start and end points."}, status=400)

    if fuel_data is None:
        return JsonResponse({"error": "Fuel prices file not found."}, status=404)

    # Aqui você pode implementar a lógica de cálculo da rota.
    response_data = {
        "start": start,
        "end": end,
        "message": "Route calculation placeholder",
        "fuel_data": fuel_data,  # Usa os dados do CSV já carregados
    }

    return JsonResponse(response_data)

def get_route(request):
    # Pegar as coordenadas de início e término da URL
    start = request.GET.get('start')  # Coordenadas de início no formato 'longitude,latitude'
    end = request.GET.get('end')  # Coordenadas de fim no formato 'longitude,latitude'

    if not start or not end:
        return JsonResponse({"error": "Coordenadas de início e fim são obrigatórias"}, status=400)

    # Converter as coordenadas de string para lista de floats
    try:
        start_coords = [float(coord) for coord in start.split(',')]
        end_coords = [float(coord) for coord in end.split(',')]
    except Exception as e:
        return JsonResponse({"error": "Coordenadas inválidas. Use o formato 'longitude,latitude'."}, status=400)

    # Definir os cabeçalhos da requisição
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }

    # Definir os dados da requisição com as coordenadas
    data = {
        "coordinates": [start_coords, end_coords],
        "profile": "driving-car",
        "format": "geojson"
    }

    # Fazer a requisição POST para obter a rota
    response = requests.post(MAPS_API_URL, json=data, headers=headers)

    if response.status_code != 200:
        return JsonResponse({"error": f"Erro ao obter rota: {response.status_code}"}, status=500)

    # Extrair dados da rota retornada
    route_data = response.json()
    distance = route_data['features'][0]['properties']['segments'][0]['distance'] / 1609.34  # Converter de metros para milhas

    # Calcular o número de abastecimentos necessários
    range_per_tank = 500  # Alcance máximo do veículo em milhas
    gallons_needed = distance / 10  # Veículo percorre 10 milhas por galão
    cost_total = gallons_needed * (fuel_data['Retail Price'].mean() if fuel_data else 0)  # Custo total com base no preço médio do CSV

    # Encontrar postos de combustível com preços mais baixos ao longo da rota
    fuel_stops = pd.DataFrame(fuel_data)
    fuel_stops = fuel_stops[fuel_stops['Retail Price'] <= fuel_stops['Retail Price'].mean()]

    return JsonResponse({
        'route_distance': distance,  # Distância total da rota
        'fuel_stops': fuel_stops[['Truckstop Name', 'Address', 'City', 'State', 'Retail Price']].to_dict(orient='records'),
        'total_cost': cost_total  # Custo total estimado de combustível
    })
