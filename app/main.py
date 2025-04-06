# app/main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from .tasks import process_heavy_operation

app = FastAPI()

class RequestPayload(BaseModel):
    user_id: str
    message: str
    # Outros campos conforme necessidade

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
