# REST API Python, JWT(Json Web Token), Django, SQLLite

## Requirements
* Python, Django

## Installation
* Clone this repo: ``` git clone https://github.com/FernandoFBueno/python-rest-jwt.git ```
* Go to installation folder ``` cd cashbackapi ```
* Install dependecies: ``` pip install -r requirements.txt ```
* Make Migrations ``` python manage.py makemigratios ```
* Migrate Database ``` python manage.py migrate ```
* Run: ``` python manage.py runserver 9000 ```

## Test
* Run: ``` python manage.py test ```

## Criar Usuario
* Post 
```js
curl --location --request POST 'http://127.0.0.1:9000/user/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Nome": "Fernando 32",
    "CPF": "30130130133",
    "Email": "teste32@teste.com",
    "Senha": "12345",
    "Super": false
}'
```

## Validar Usuario
* Get 
```js
curl --location --request GET 'http://127.0.0.1:9000/validate-login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Email": "teste32@teste.com",
    "Senha": "12345"
}'
```

## Autenticar Usuario
* Post 
```js
curl --location --request POST 'http://127.0.0.1:9000/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "30130130133",
    "password": "12345"
}'
```
* Retorno Token, guardar o token
```js
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjMwMTMwMTMwMTMzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0ZTMyQHRlc3RlLmNvbSIsImV4cCI6MTU5Mzg3MTI1Nn0.4s9Vzh3-L864gjeLFOrK18ObuStizEGsltGP2k_dZSc"
}
```

## Listar Todos os Revendedores
* Get com Token 
```js
curl --location --request GET 'http://127.0.0.1:9000/revendedores/' \
--header 'Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjMwMTMwMTMwMTMzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0ZTMyQHRlc3RlLmNvbSIsImV4cCI6MTU5Mzg3MTI1Nn0.4s9Vzh3-L864gjeLFOrK18ObuStizEGsltGP2k_dZSc'
```

## Listar um Revendedor
* Get com Token 
```js
curl --location --request GET 'http://127.0.0.1:9000/revendedor/2' \
--header 'Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjMwMTMwMTMwMTMzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0ZTMyQHRlc3RlLmNvbSIsImV4cCI6MTU5Mzg3MTU5NH0.M-JaSm0IcwPHan2bp6hoXQJK_bspLhXqwBpezp-PVV8'
```

## Criar Faixas de Cash Back
* Post com Token 
```js
curl --location --request POST 'http://127.0.0.1:9000/faixas-cashback/' \
--header 'Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjMwMTMwMTMwMTMzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0ZTMyQHRlc3RlLmNvbSIsImV4cCI6MTU5Mzg3MTI1Nn0.4s9Vzh3-L864gjeLFOrK18ObuStizEGsltGP2k_dZSc' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Descricao": "Compras acima de R$ 1500",
    "Porcentagem": 20,
    "FaixaTop": 10000,
    "FaixaIni": 1500.01
}'
```

```js
curl --location --request POST 'http://127.0.0.1:9000/faixas-cashback/' \
--header 'Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjMwMTMwMTMwMTMzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0ZTMyQHRlc3RlLmNvbSIsImV4cCI6MTU5Mzg3MTI1Nn0.4s9Vzh3-L864gjeLFOrK18ObuStizEGsltGP2k_dZSc' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Descricao": "Compras até R$ 1500",
    "Porcentagem": 15,
    "FaixaTop": 1500,
    "FaixaIni": 1000.01
}'
```

```js
curl --location --request POST 'http://127.0.0.1:9000/faixas-cashback/' \
--header 'Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjMwMTMwMTMwMTMzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0ZTMyQHRlc3RlLmNvbSIsImV4cCI6MTU5Mzg3MTI1Nn0.4s9Vzh3-L864gjeLFOrK18ObuStizEGsltGP2k_dZSc' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Descricao": "Compras até R$ 1000",
    "Porcentagem": 10,
    "FaixaTop": 1000,
    "FaixaIni": 0
}'
```

## Criar Compra
* Post com Token 
```js
curl --location --request POST 'http://localhost:8080/api/v1/compra' \
--header 'x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVlZmY5NGNjMjVkMjA2NWQ5NDA0Y2NlYiIsImlhdCI6MTU5MzgxODEyNywiZXhwIjoxNTkzODIxNzI3fQ.1K8higWtsuIzVCI5iJJeGJejkQtm5HMsCo-X81qgZ7s' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Revendedor": "5efd31c8e44149beb973dc36",
    "ValorCompra": 500.56
}'
```

## Listar todas as compras
* Get com Token 
```js
curl --location --request GET 'http://127.0.0.1:9000/compras/' \
--header 'Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjMwMTMwMTMwMTMzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0ZTMyQHRlc3RlLmNvbSIsImV4cCI6MTU5Mzg3MTI1Nn0.4s9Vzh3-L864gjeLFOrK18ObuStizEGsltGP2k_dZSc'
```

## Listar todas as compras por revendedor
* Get com Token passando o cpf do revendedor
```js
curl --location --request GET 'http://127.0.0.1:9000/compras-revendedor/' \
--header 'Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjMwMTMwMTMwMTMzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0ZTMyQHRlc3RlLmNvbSIsImV4cCI6MTU5Mzg3MTkyOX0.8PaF2Mvdsi7iVC4M0Y02xer09po-vhyZlkkx-nag6OE' \
--header 'Content-Type: application/json' \
--data-raw '{
    "cpf": "12312312322"
}'
```

## Total de CashBack
* Get com Token passando o cpf do revendedor
```js
curl --location --request GET 'http://127.0.0.1:9000/cashback/' \
--header 'Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjMwMTMwMTMwMTMzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0ZTMyQHRlc3RlLmNvbSIsImV4cCI6MTU5Mzg3MjMxOX0.dPJ0bUehKzsAPV1XIxD6GEXuxEY08XNzUlycaRchb24' \
--header 'Content-Type: application/json' \
--data-raw '{
    "cpf": "12312312322"
}'
```


