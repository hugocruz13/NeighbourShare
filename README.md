# NeighbourShare

NeighbourShare é um projeto prático desenvolvido para as unidades curriculares de **PDS (Projeto de Desenvolvimento de Software)** e **Programação Web**. O objetivo deste projeto é criar uma aplicação colaborativa que permite aos utilizadores compartilhar e solicitar recursos dos seus vizinhos, promovendo a cooperação e o senso de comunidade.


## Instruções para utilizar os Containers com Docker

### Pré-requisitos

Antes de executar os containers, é necessário garantir que tens os seguintes requisitos instalados na tua máquina:

1. **Docker**:
   - Instala o Docker Desktop [aqui](https://www.docker.com/products/docker-desktop).

3. **Autenticação no GitHub Container Registry** (para imagens privadas):
   - Como a imagem está armazenada no GitHub Container Registry (GHCR), será necessário autenticar o Docker para aceder à imagem. Para isso, faz login na tua conta GitHub.

   **Login no GHCR**:
   ```bash
   docker login ghcr.io -u <seu-nome-utilizador> -p <token-de-acesso-pessoal>
   ```
   Substitui `<seu-nome-de-utilizador>` pelo teu nome de utilizador do GitHub e `<token-de-acesso-pessoal>` pelo token de acesso gerado nas configurações da tua conta GitHub.

---

### Passo 1: Clonar o Repositório

Primeiro, faz o clone do repositório para a tua máquina local:

```bash
git clone <url-do-repositorio>
```

Exemplo:
```bash
git clone https://github.com/mtcigor/NeighbourShare.git
```

Entra no diretório do projeto:

```bash
cd NeighbourShare
```

---

### Passo 2: Construir e Subir os Containers com Docker

Dentro do diretório do projeto, utiliza o seguinte comando para construir e subir os containers:

```bash
docker-compose up --build
```

O comando acima fará o seguinte:
- **`--build`**: Força a construção das imagens, caso as mesmas não estejam construídas ou se existirem alterações no código.
- O Docker Compose irá criar os containers definidos no arquivo `docker-compose.yml`.

---

### Passo 3: Aceder aos Containers

#### Aceder à API (FastAPI)
O backend da aplicação (FastAPI) estará disponível na porta **8000**.

- URL: [http://localhost:8000](http://localhost:8000)

#### Aceder à Web App (React)
O frontend da aplicação (React) estará disponível na porta **80**.

- URL: [http://localhost:80](http://localhost:80)

#### Aceder ao SQL Server
A base de dados SQL Server estará disponível na porta **1433**. Para aceder à base de dados, podes usar qualquer ferramenta SQL, como o [SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms).

As credenciais de acesso são:

- **Servidor**: `localhost,1433`
- **Utilizador**: `sa`
- **Senha**: `DEVesi2025`
- **Base de dados**: `NeighbourShare`

---

### Passo 4: Parar os Containers

Para parar os containers, usa o comando:

```bash
docker-compose down
```

Este comando irá parar e remover os containers, mas irá manter os volumes de dados. Caso também queiras remover os volumes, podes usar:

```bash
docker-compose down -v
```

---

### Passo 5: Logs dos Containers

Para visualizar os logs de execução dos containers, usa o seguinte comando:

```bash
docker-compose logs
```

Ou para visualizar os logs de um container específico, por exemplo, o backend:

```bash
docker-compose logs backend
```

---

### Passo 6: Reiniciar os Containers

Se precisas de reiniciar os containers, podes usar:

```bash
docker-compose restart
```

---

### Passo 7: Outros Comandos Úteis

- **Listar os containers em execução**:
  ```bash
  docker ps
  ```

- **Listar todas as imagens Docker**:
  ```bash
  docker images
  ```

- **Remover containers parados**:
  ```bash
  docker container prune
  ```

- **Remover imagens não usadas**:
  ```bash
  docker image prune
  ```

---


## Como atualizar o package com uma nova imagem

### 1. Criar a imagem
Para criar uma nova imagem a partir de um container em execução, usa o comando
`docker commit`:

	`docker commit <nome-container> <nome-imagem>`
 
 Substitui `<nome-container>` pelo nome ou ID do teu container em execução e `<nome-imagem>` pelo nome que desejas dar à tua nova imagem. 
	
### 2. Login no GitHub Container Registry (GHCR)
Para enviar a imagem para o GitHub Container Registry, primeiro é necessário fazer login utilizando um token de acesso. Executa o seguinte comando:

	`echo "Token-Git" | docker login ghcr.io -u <user-git> --password-stdin`

Substitui `"Token-Git"` pelo teu token de acesso do GitHub e `<user-git>` pelo teu nome de utilizador do GitHub.
 
### 3. Criar uma tag para a imagem
Depois de criares a imagem, adiciona uma tag que identifique a versão. Usa o comando `docker tag`:

	docker tag <nome-imagem> ghcr.io/mtcigor/neighbourshare-db:V<versao>

Substitui `<nome-imagem>` pelo nome da imagem que criaste e `<versao>` pela versão que desejas atribuir à imagem (por exemplo, v1.0.1).

### 4. Carregar a imagem para o repositório do GHCR
Por fim, para enviar a imagem para o GitHub Container Registry, usa o comando `docker push`:

	docker push ghcr.io/mtcigor/neighbourshare-db:V<versao>

 Substitui `<versao>` pela versão que usaste na etapa anterior.
