# Fuel Route API

Este projeto é uma API que calcula rotas de direção e ajuda a identificar os melhores locais para reabastecimento de acordo com os preços de combustível em um trajeto. A API utiliza dados de preços de combustível de um arquivo CSV e informações de rotas da API OpenRouteService.

## Funcionalidades

- Calcula a rota entre dois pontos com base em coordenadas geográficas. http://127.0.0.1:8000/route/get_route/?start=-73.935242,40.730610&end=-118.243683,34.052235
- Mostra o custo total estimado da viagem com base nos preços de combustível. http://127.0.0.1:8000/route/get_route/?start=-73.935242,40.730610&end=-118.243683,34.052235
- Encontra os melhores postos de abastecimento ao longo da rota. http://127.0.0.1:8000/route/get_route/?start=-73.935242,40.730610&end=-118.243683,34.052235
X- Gera um mapa da rota usando Folium. nao esta gerando o map.html e ligacao dos dados do retorno/api http://localhost:8000/route/?start=-73.935242,40.730610&end=-118.243683,34.052235
X admin criar username e senha -http://localhost:8000/admin/login/?next=/admin/
-puxa dados do .csv http://localhost:8000/route/fuel-data/

video do projeto - https://www.loom.com/share/26f8e9e1a1944cbe8dec5eca25f2b398?sid=47db71c3-73de-4ace-9cd4-25697589f6fc
## Pré-requisitos

Antes de rodar o projeto, certifique-se de que você tem os seguintes itens instalados:

## Como Rodar o Projeto

Siga os passos abaixo para rodar este projeto em sua máquina local.

- **Python 3.8 ou superior**: Certifique-se de ter o Python instalado em sua máquina. Você pode baixá-lo [aqui](https://www.python.org/downloads/).
- **Pip**: O gerenciador de pacotes do Python, normalmente vem junto com a instalação do Python.
- **Django 3.2.23**: O framework web utilizado neste projeto.
- **Pandas**: Biblioteca para manipulação de dados.
- **Requests**: Biblioteca para fazer chamadas de API.
- **Folium**: Biblioteca para gerar mapas.
- **Plotly**: Biblioteca para visualizações interativas.
## Instalação

1. Clone este repositório:

    ```bash
    git clone https://github.com/seu-usuario/fuel-route-api.git
    ```

2. Navegue até o diretório do projeto:

    ```bash
    cd fuel-route-api
    ```

3. Crie e ative um ambiente virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    .\venv\Scripts\activate  # Para Windows
    ```

4. Instale as dependências do projeto:

    ```bash
    pip install -r requirements.txt

    ## Licença

5. Configure o banco de dados

 Este projeto não utiliza um banco de dados externo por padrão. O banco de dados SQLite será criado automaticamente ao rodar as migrações.

Para rodar as migrações e configurar o banco de dados, execute:

bash

python manage.py migrate


6. Adicione as chaves de API necessárias

Certifique-se de que você tem a API Key da OpenRouteService e outras integrações que você deseja utilizar, como o GasBuddy. Essas chaves podem ser definidas diretamente no código ou em variáveis de ambiente.

7. Carregue os dados de preços de combustível

Coloque o arquivo fuel_prices.csv com os dados de preços de combustível na raiz do projeto ou ajuste o caminho no código para apontar para o arquivo correto.

8. Inicie o servidor

Agora, você pode rodar o servidor local do Django:

bash
python manage.py runserver
O servidor irá rodar por padrão no endereço http://localhost:8000/.

9. Acesse o projeto

Abra seu navegador e acesse:


http://localhost:8000
Para testar a rota de busca, acesse o link:


http://localhost:8000/route/get_route/?start=<longitude,latitude>&end=<longitude,latitude>

Exemplo de URL:

http://localhost:8000/route/get_route/?start=-122.4194,37.7749&end=-73.9352,40.7306

Observações
Caso você queira modificar os dados de combustível, edite o arquivo fuel_prices.csv ou faça a integração com APIs externas, como mencionado nas melhorias futuras.

Verifique as mensagens de log no terminal para garantir que o servidor e os cálculos estejam sendo executados corretamente.

resumo:
Essa seção fornece instruções detalhadas para configurar e rodar o projeto na máquina local, desde a clonagem do repositório até a execução do servidor Django e acesso às rotas da API.
=============///=================

Aqui está uma explicação detalhada dos endpoints do seu projeto, baseada nas rotas que você configurou nos arquivos `urls.py` e `views.py`.

### Estrutura de URLs

#### Arquivo `urls.py` principal (nível do projeto)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Acesso ao painel de administração do Django
    path('route/', include('routes.urls')),  # Inclui as rotas da aplicação "routes"
]
```

Aqui temos a estrutura principal de rotas do projeto:

- **`admin/`**: O caminho padrão para acessar o painel administrativo do Django. Este endpoint é gerado automaticamente pelo Django e permite o gerenciamento de dados e modelos da aplicação.
  
- **`route/`**: Este caminho inclui todas as rotas da aplicação "routes", que são definidas separadamente no arquivo `routes/urls.py`.

#### Arquivo `urls.py` da aplicação `routes`

```python
from django.urls import path
from . import views  # Importa as views da aplicação
from .views import display_fuel_data, home, route_view

urlpatterns = [
    path('', views.home, name='home'),  # Rota para a página inicial
    path('get_route/', views.get_route, name='get_route'),  # Rota para obter a rota
    path('route/', route_view, name='route_view'),  # View que renderiza rota e exibe detalhes
    path('fuel-data/', display_fuel_data, name='fuel_data'),  # Rota para exibir os dados de combustível
]
```

Aqui estão definidas as rotas específicas da sua aplicação, cada uma ligada a uma view responsável por processar a lógica e retornar os dados.

### Endpoints Explicados

#### 1. **Página inicial (`/`)**

- **Endpoint**: `''` (raiz da aplicação)
- **View associada**: `views.home`
- **Método HTTP**: `GET`
- **Descrição**: Renderiza a página inicial (`home.html`). É a rota principal que será acessada quando alguém visitar a aplicação sem fornecer uma rota específica. Pode ser usada como uma página de boas-vindas ou como ponto de entrada para outras funcionalidades.
  
#### 2. **Obter rota de viagem (`/get_route/`)**

- **Endpoint**: `/route/get_route/`
- **View associada**: `views.get_route`
- **Método HTTP**: `GET`
- **Parâmetros esperados**:
  - `start`: Coordenadas de início no formato `longitude,latitude` (por exemplo, `-122.4194,37.7749`).
  - `end`: Coordenadas de fim no formato `longitude,latitude` (por exemplo, `-73.9352,40.7306`).
  
- **Descrição**: Este endpoint faz a busca de uma rota entre os pontos de início e fim fornecidos via parâmetros GET (`start` e `end`). Ele utiliza a API do OpenRouteService para calcular a rota, e também retorna o custo estimado da viagem e os locais de abastecimento ao longo do percurso.

  Exemplo de requisição:
  
  ```
  http://localhost:8000/route/get_route/?start=-122.4194,37.7749&end=-73.9352,40.7306
  ```

- **Retorno**:
  - JSON com a distância da rota, o custo total de combustível e os postos de abastecimento recomendados.
  - Exemplo de resposta:
    ```json
    {
        "route_distance": 3000.0,
        "total_amount": 500.0,
        "fuel_stops": [
            {
                "Truckstop_Name": "Posto 1",
                "Address": "Endereço 1",
                "City": "Cidade 1",
                "State": "Estado 1",
                "Retail_Price": "4.50"
            }
        ],
        "total_cost": 300.0
    }
    ```

#### 3. **Visualizar dados da rota com template (`/route/`)**

- **Endpoint**: `/route/`
- **View associada**: `views.route_view`
- **Método HTTP**: `GET`
- **Parâmetros esperados**:
  - `start`: Coordenadas de início no formato `longitude,latitude`.
  - `end`: Coordenadas de fim no formato `longitude,latitude`.
  
- **Descrição**: Este endpoint processa uma requisição de rota similar ao `/get_route/`, mas ao invés de retornar um JSON diretamente, renderiza um template HTML (`home.html`) com os detalhes da rota. É útil para usuários que desejam uma interface visual com informações sobre a rota e custos.
  
  Exemplo de requisição:
  ```
  http://localhost:8000/route/?start=-122.4194,37.7749&end=-73.9352,40.7306
  ```

- **Retorno**: Renderiza a página `home.html` com os seguintes dados:
  - `route_distance`: A distância da rota.
  - `total_cost`: O custo estimado de combustível.
  - `fuel_stops`: Lista de paradas de combustível recomendadas.

#### 4. **Visualizar dados de combustível (`/fuel-data/`)**

- **Endpoint**: `/route/fuel-data/`
- **View associada**: `views.display_fuel_data`
- **Método HTTP**: `GET`
- **Descrição**: Este endpoint retorna os dados de combustível armazenados no arquivo `fuel_prices.csv`. Ele pode ser utilizado para visualizar os preços de combustível disponíveis para cálculo nas rotas.
  
- **Retorno**:
  - JSON com uma lista de postos de combustíveis e seus preços.
  - Exemplo de resposta:
    ```json
    [
      {
        "Truckstop Name": "Posto 1",
        "Address": "Rua 1",
        "City": "Cidade 1",
        "State": "Estado 1",
        "Retail Price": "4.50"
      },
      {
        "Truckstop Name": "Posto 2",
        "Address": "Rua 2",
        "City": "Cidade 2",
        "State": "Estado 2",
        "Retail Price": "4.75"
      }
    ]
    ```

### Conclusão

- O projeto possui endpoints para buscar e visualizar rotas otimizadas, cálculos de custos de combustível e paradas recomendadas para abastecimento ao longo da viagem.
- A estrutura é modular, permitindo a expansão para novos endpoints ou funcionalidades.
- As views utilizam a API do OpenRouteService para calcular rotas, enquanto os dados de combustível vêm de um arquivo CSV local.



Este projeto é licenciado sob os termos da licença MIT. Você pode conferir mais detalhes no arquivo `LICENSE`.

## Melhorias Futuras

Algumas funcionalidades que podem ser adicionadas ao projeto no futuro:

1. **Integração com mais APIs de preços de combustível**: Atualmente, os preços são carregados de um arquivo CSV, mas a integração com APIs em tempo real (como a EIA API ou GasBuddy) permitiria que o sistema sempre utilizasse os preços mais recentes.

2. **Otimização de rota considerando os preços de combustível**: Implementar a funcionalidade de encontrar a rota mais econômica, considerando não apenas a distância, mas também os preços de combustível ao longo da rota.

3. **Suporte a diferentes perfis de veículos**: Permitir que o usuário informe dados como o consumo de combustível e capacidade do tanque do veículo para cálculos mais precisos.

4. **Geração de relatórios**: Gerar relatórios detalhados da viagem, incluindo os postos de combustível visitados e os preços pagos.

5. **Mapas interativos com informações dos postos**: Adicionar pop-ups nos mapas gerados com informações detalhadas sobre os postos de combustível e os preços.

6. **Autenticação e personalização**: Implementar um sistema de autenticação de usuários para que possam salvar rotas, ver histórico de viagens, e personalizar suas preferências de reabastecimento.

7. Transformar sua API local em um servidor acessível a partir de outros dispositivos

## Contato

Se você tiver alguma dúvida ou sugestão, entre em contato através do seguinte e-mail: jonatha.mendonca@hotmail.com

## Agradecimentos

Gostaríamos de agradecer às seguintes tecnologias e serviços que tornaram este projeto possível:

- [Django](https://www.djangoproject.com/)
- [OpenRouteService API](https://openrouteservice.org/sign-up/)
- [Pandas](https://pandas.pydata.org/)
- [Folium](https://python-visualization.github.io/folium/)
- [Plotly](https://plotly.com/python/)

---
Esperamos que este projeto seja útil e estamos abertos a melhorias e sugestões. Aproveite!


    
