FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src


COPY API/API.csproj API/
COPY BLL/BLL.csproj BLL/
COPY DAL/DAL.csproj DAL/
COPY Models/Models.csproj Models/

# Restaura as dependências de todos os projetos
RUN dotnet restore "./API/API.csproj"

# Copia o restante dos arquivos do projeto
COPY . .

# Trabalha na pasta do projeto RESTful-API
WORKDIR "/src/API"
RUN dotnet build "./API.csproj" -c $BUILD_CONFIGURATION -o /app/build

# Este estágio é usado para publicar o projeto de serviço
FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./API.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

# Este estágio é usado na produção ou quando executando normalmente
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
USER $APP_UID
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

# Copia os arquivos publicados para o contêiner final
COPY --from=publish /app/publish .

# Define o ponto de entrada para o contêiner
ENTRYPOINT ["dotnet", "API.dll"]
