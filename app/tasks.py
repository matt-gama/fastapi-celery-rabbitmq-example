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
