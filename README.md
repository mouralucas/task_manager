# Aplicação de lista de tarefas
## By Lucas Moura

Contato: lucaspenha471@gmail.com

Github: [@mouralucas](https://github.com/mouralucas)

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
curl --location http://127.0.0.1:8000/task
```

### Criar uma nova tarefa:

```bash
curl --location http://127.0.0.1:8000/task \
--header 'Content-Type: application/json' \
--data {
    "date": "2024-12-01T08:00:00-03:00",
    "description": "Essa é uma tarefa"
}
```

### Concluir uma tarefa:

```bash
curl --location --request PATCH 'http://127.0.0.1:8000/task/complete' \
--header 'Content-Type: application/json' \
--data '{
    "taskId": "3ee208f4891c45aa9bb491874110ca32"
}'
```

Obs: para concluir uma tarefa, o 'taskId' deve ser substituído pelo taskId de uma tarefa criada anteriormente
O ID apresentado acima é apenas um exemplo


### Apagar uma tarefa:
```bash
curl --location --request DELETE 'http://127.0.0.1:8000/task' \
--header 'Content-Type: application/json' \
--data '{
    "taskId": "be3dd5fd017b4e52a3c70219c5a1e050"
}'
```

Obs: para concluir uma tarefa, o 'taskId' deve ser substituído pelo taskId de uma tarefa criada anteriormente
O ID apresentado acima é apenas um exemplo