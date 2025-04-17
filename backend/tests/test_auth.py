from db.models import Utilizador

def test_registar_utilizador(client, db_session, token_admin):

    user_data = {
        "email": "newuser@gmail.com",
        "role": "residente"
    }

    response = client.post(
        "/api/registar",
        json=user_data,
        cookies={"access_token": token_admin}  # Passando o token no cookie
    )

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.json()}")  # Imprime o conteúdo da resposta para diagnóstico

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["message"] == "Registo realizado com sucesso"

    db_user = db_session.query(Utilizador).filter(Utilizador.Email == user_data["email"]).first()
    assert db_user is not None
    assert db_user.Email == user_data["email"]