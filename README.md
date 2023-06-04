# Repositório do back-end do projeto 3 da disciplina TecWeb
## Insper 2023.1

# Tocket: Marketplace de Ingressos

## Link para o cronograma das sprints (Trello): 

https://trello.com/invite/b/wwXDUy10/ATTI55c9caf90ef9097b5eebfd95d656bca7FCB3C812/arthurcaiogabrielpedroprojeto3tecweb

## Arquitetura do Projeto

![ArquiteturaTocket](https://github.com/CaioBoa/tocket-backend/assets/67804009/49c08faa-068e-422b-8a9e-924a74405519)


## Instruções para rodar o código:

### Back-end:

#### Rodar os seguintes comandos no terminal da pasta:

python3 -m venv env

env\Scripts\Activate.ps1

pip install -r requirements.txt

python manage.py runserver

### Front-end:

#### Rodar os seguintes comandos no terminal da pasta:

npm install

npm run dev

## Link para o vídeo de demonstração do projeto:

https://youtu.be/OPneu685t9s

## Observações:

### API Poke_Event

A api utiliza uma chave do chat GPT e para evitar usos desnecessários a chave se encontra desativada no período de testes, possuíndo o pokémon  pichu como placeholder. Para o caso de apenas o pokémon pichu aparecer para os eventos do site é necessário alterar a chave UseKey para True.

Tal chave se encontra no seguinte local events/views.py , na primeira linha de código da função poke_event.
