import httpx
import time

API_URL = "http://localhost:8000/"
WEB_URL = "http://localhost:80/"

def test_api_response_time():
    start = time.time()
    response = httpx.get(f"{API_URL}api/health")
    end = time.time()
    
    duration = (end - start) * 1000  # em milissegundos
    assert response.status_code == 200
    assert duration < 200, f"Tempo de resposta para API excedeu 200ms: {duration:.2f}ms"

def test_web_response_time():
    start = time.time()
    response = httpx.get(f"{WEB_URL}")
    end = time.time()
    
    duration = (end - start) * 1000  # em milissegundos
    assert response.status_code == 200
    assert duration < 400, f"Tempo de resposta para website excedeu 400ms: {duration:.2f}ms"