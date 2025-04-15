from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        login_payload = {
            "email": "teste@exemplo.com",
            "password": "123456"
        }
        response = self.client.post("/api/login", json=login_payload)

        if response.status_code == 200:
            print("Autenticado com sucesso")
        else:
            print(f"Erro ao autenticar: {response.status_code} - {response.text}")

    #TODO Colocar as requisições aos recursos (por exemplo) a funcionar
    @task
    def testar_endpoint_recursos(self):
        self.client.get("/api/recursos/pessoais")