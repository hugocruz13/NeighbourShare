# NeighbourShare
Repositório para o desenvolvimento do projeto prático para a cadeira de PDS e Programação Web


## Docker

### 1. Criar a imagem
	docker commit <nome-container> <nome-imagem>
	
### 2. Login no GitHub Container Registry (GHCR)
	echo "Token-Git" | docker login ghcr.io -u <user-git> --password-stdin
	
### 3. Tag para a imagem
	docker tag <nome-imagem> ghcr.io/mtcigor/neighbourshare-db:V<versao>

### 4. Carregar a imagem para o repositório do GHCR
	docker push ghcr.io/mtcigor/neighbourshare-db:V<versao>

## Gerar imagem backend
	
### Criar Imagem
	docker build -t backend .

### Executar 
	docker run -d -p 8080:8080 --name backend backend
