# Aplicação de lista de tarefas
## By Lucas Moura

Contato: lucaspenha471@gmail.com

Github: [@mouralucas](https://github.com/mouralucas)


Aplicativo desenvolvido em FastAPI, bastante similar ao Flask. Utilizei esse framework 
para usar das chamadas assíncronas nativas dele e da simplicidade de configuração.

## Requisitos mínimos

1. [Docker](https://docs.docker.com/engine/install/)
2. [docker-compose](https://docs.docker.com/compose/install/)


## Docker
Para rodar o código, basta entrar na raiz do projeto e rodar os seguintes comandos:

```bash
docker-compose build --no-cache
```

```bash
docker-compose up
```

## Exemplos de chamadas

### Lista todos as tarefas:

```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/task' \
  -H 'accept: application/json'
```

### Criar uma nova tarefa:

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/task' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "date": "2024-12-05T13:06:16.774Z",
  "description": "Outra Tarefa de teste"
}'
```

### Concluir uma tarefa:

```bash
curl -X 'PATCH' \
  'http://0.0.0.0:8000/task/complete' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "taskId": "4ea1de05-743a-4218-bf4e-eaf90d602914"
}'
```

Obs: para concluir uma tarefa, o 'taskId' deve ser substituído pelo taskId de uma tarefa criada anteriormente
O ID apresentado acima é apenas um exemplo


### Apagar uma tarefa:
```bash
curl -X 'DELETE' \
  'http://0.0.0.0:8000/task' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "taskId": "4ea1de05-743a-4218-bf4e-eaf90d602914"
}'
```

Obs: para concluir uma tarefa, o 'taskId' deve ser substituído pelo taskId de uma tarefa criada anteriormente
O ID apresentado acima é apenas um exemplo