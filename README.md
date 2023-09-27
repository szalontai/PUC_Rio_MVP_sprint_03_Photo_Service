# Componente C - Microserviço de gestão de fotos

Este projeto faz parte do material didático da Disciplina **Arquitetura de Software - Sprint 3** 

O objetivo desta API é a gestão de fotos seguindo o estilo REST.
---

### Instalação


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.


> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Para gerar o arquivo `requirements.txt` rode o comando abaixo.

```
(env)$ pip freeze > requirements.txt
```
O comando abaixo instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

```
(env)$ pip install -r requirements.txt
```

### Executando o servidor


Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5030
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5030 --reload
```

---
### Acesso no browser

Abra o [http://localhost:5030/#/](http://localhost:5030/#/) no navegador para verificar o status da API em execução.

---
## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t photo-service .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5030:5030 photo-service
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5030/#/](http://localhost:5030/#/) no navegador.
