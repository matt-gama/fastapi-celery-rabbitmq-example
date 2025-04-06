# 📦 Projeto FastAPI + Celery + RabbitMQ

Este projeto demonstra uma aplicação **FastAPI** que recebe requisições HTTP e executa tarefas assíncronas usando **Celery** com o broker **RabbitMQ**.

---

## 🚀 Estrutura do Projeto

```
fastapi-celery-rabbitmq-example/
│
├── app/
│   ├── main.py              # FastAPI app
│   ├── celery_app.py        # Instância do Celery
│   └── tasks.py             # Tarefas assíncronas
│
├── requirements.txt
└── README.md
```

---

## 🔧 Exemplo Prático

### `app/main.py`
```python

@app.post("/")
async def receive_zapi(payload: RequestPayload):
    """
    Endpoint que recebe a requisição e publica a tarefa para ser processada pelos workers.
    Retorna 200 imediatamente, dizendo que a requisição foi aceita.
    """
    # 1. Aqui você pode fazer validações rápidas, logs, etc.
    data_dict = payload.dict()

    # 2. Chama a task Celery de forma assíncrona
    print(data_dict)
    process_heavy_operation.delay(data_dict) 
    # .delay() = dispara a tarefa no broker RabbitMQ, sem bloquear

    # 3. Retorna imediatamente
    return {"status": "accepted", "data_received": data_dict}
```

---

### `app/celery_app.py`
```python

import os
from celery import Celery

broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
publisher = os.getenv("PUBLISHER", "default")

celery = Celery(
    "my_celery_app",
    broker=broker_url,
    backend=None,
    include=["app.tasks"]  # <--- ADICIONE ESTA LINHA
)

celery.conf.update({
    "task_default_queue": publisher,
    "worker_concurrency": 4,
})
```

---

### `app/tasks.py`
```python
from .celery_app import celery
import time

@celery.task
def process_heavy_operation(data: dict):
    """
    Exemplo de função que será executada em segundo plano pelos workers.
    Pode ser chamada diretamente do Microserviço A.
    """
    # Simular trabalho pesado (CPU-bound ou I/O)
    time.sleep(5)  # Exemplo de espera
    # Aqui você faria integrações com IA, supabase, etc.
    print(f"[Worker] Processando data: {data}")
    return {"status": "done", "processed_data": data}

```

---

## 🧪 Como Rodar o Projeto

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### `requirements.txt`
```
fastapi
uvicorn
celery
pika
flower
```

---

## 🐇 Subindo o RabbitMQ com Docker (opcional)
```bash
docker run -d --hostname my-rabbit --name some-rabbit \
    -p 5672:5672 -p 15672:15672 \
    -e RABBITMQ_DEFAULT_USER=usuario \
    -e RABBITMQ_DEFAULT_PASS=senha \
    rabbitmq:3-management
```

> Acesse o painel do RabbitMQ: http://localhost:15672

---

## 🔥 Rodando os serviços

### Iniciar o servidor FastAPI em modo debug
```bash
uvicorn app.main:app --reload
```

### Iniciar o worker Celery
```bash
celery -A app.celery_app:celery worker --pool=solo --loglevel=info -n worker1@h --concurrency=4
```

### Iniciar o monitor Flower
```bash
celery -A app.celery_app:celery flower --basic_auth=user:password --port=5555
```

> ⚠️ **IMPORTANTE:** Altere `user:password` para valores seguros em produção.

---

## 📈 Escalando a API com Celery

Você pode escalar criando múltiplos workers em paralelo:

```bash
celery -A app.celery_app:celery worker --loglevel=info -n worker2@h --concurrency=4
celery -A app.celery_app:celery worker --loglevel=info -n worker3@h --concurrency=4
```

Ou usando `autoscaling` com supervisores como `supervisord`, `systemd` ou Docker Compose/Kubernetes.

---

## ✅ Testando a API

Faça um `POST` para a rota:

```
POST http://localhost:8000/processar/
Content-Type: application/json

{
  "dado": "valor importante"
}
```

A resposta será imediata:
```json
{"message": "Tarefa recebida e está sendo processada."}
```

E o processamento ocorrerá no Celery.

---

## 🛡️ Segurança

- Altere o `usuario:senha` no `celery_app.py` e nas variáveis de ambiente do RabbitMQ.
- Não exponha o Flower sem autenticação ou via HTTPS.
- Use variáveis de ambiente (ex: com `python-dotenv`) para senhas e configs sensíveis.

---

## 🧹 Futuras melhorias

- Adicionar `.env` para configs
- Deploy com Docker Compose
- Tasks encadeadas, retries, timeouts
- Integração com Redis como resultado e cache

