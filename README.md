# Loja API

### Este projeto é uma API RESTful desenvolvida com FastAPI, com o objetivo de fornecer funcionalidades para gerenciamento de produtos em uma loja. A aplicação permite criar, listar, atualizar e remover produtos, além de oferecer uma integração com um banco de dados PostgreSQL.

## Funcionalidades
CRUD de Produtos: Criação, leitura, atualização e deleção de produtos.
Autenticação: (Se aplicável) Implementação de autenticação para proteger rotas.

Documentação Automática: A API usa a documentação Swagger integrada do FastAPI.

```
Estrutura do projeto:

loja_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── crud.py
│   └── product.py
│
├── env/ (Virtual enviroment)


# app/: Contém o código principal da aplicação.
# main.py: Arquivo principal que inicia o servidor FastAPI.
# models.py: Define as classes do SQLAlchemy para representar o banco de dados.
# schemas.py: Define os esquemas de validação de dados usando Pydantic.
# crud.py: Funções para manipulação do banco de dados.
# database.py: Configura a conexão com o banco de dados PostgreSQL.
# routers.py: Rotas organizadas para operações da API.
```

## Requisitos
```
Python 3.8+
FastAPI
SQLAlchemy
PostgreSQL
```

## Instalação

### Clone o repositório

``` 
git clone https://github.com/victorbbrito/loja_api.git
```
```
cd loja_api
```

### Crie e ative um ambiente virtual

Windows:

```
python -m venv env
```
```
.\env\Scripts\activate
```

Linux/Mac:

```
python3 -m venv env
```
```
source env/bin/activate
```
### Instale as dependências

```
pip install -r requirements.txt
```
* Configure o banco de dados PostgreSQL, editando as credenciais em database.py.

### Inicie o servidor local:
```
uvicorn app.main:app --reload
```

### Acesse a documentação interativa em

```
http://127.0.0.1:8000/docs
```

### Rotas Principais
- GET /products/: Retorna a lista de produtos.
- POST /products/: Cria um novo produto.
- PUT /products/{id}: Atualiza um produto existente.
- DELETE /products/{id}: Remove um produto.

###  Contribuições
Sinta-se à vontade para abrir issues ou pull requests para melhorias.
