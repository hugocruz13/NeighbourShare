import httpx
import time

BASE_URL = "http://localhost:8000"  # Ou o teu URL base no Docker

def test_root_response_time():
    start = time.time()
    response = httpx.get(f"{BASE_URL}/")
    end = time.time()
    
    duration = (end - start) * 1000  # em milissegundos
    assert response.status_code == 200
    assert duration < 200, f"Tempo de resposta excedeu 200ms: {duration:.2f}ms"