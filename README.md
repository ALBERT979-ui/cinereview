# CineReview

Uma aplicação web para cadastro, visualização e gerenciamento de resenhas de filmes e séries.

## Sobre o projeto

O **CineReview** é uma aplicação web desenvolvida para permitir o cadastro, a consulta e a organização de resenhas críticas de filmes e séries.

O sistema permite que o usuário registre avaliações contendo o nome do filme ou série, o ano de seu  lançamento, uma nota (de 0 até 10) e uma análise escrita (a resenha), apresentando as informações de forma organizada e intuitiva.

O projeto foi desenvolvido utilizando o padrão arquitetural **MVC (Model-View-Controller)**, separando as responsabilidades da aplicação entre Modelos, Controladores (que ainda estão integrados ao app.py junto ao Flask) e Visualizações, proporcionando uma melhor organização e manutenção do código.

## Funcionalidades

O sistema possui as seguintes funcionalidades:

- Cadastro de resenhas de filmes ou séries;
- Listagem das resenhas cadastradas;
- Sistema de notas de 0 a 10;
- Pesquisa por nome do filme ou série;
- Filtro por nota;
- Ordenação das resenhas por:
  - Mais recentes
  - Mais antigas
  - Ordem alfabética
- Exibição da data de criação da resenha;
- Interface utilizando cards para apresentação das avaliações;
- Persistência dos dados utilizando PostgreSQL;
- Arquitetura MVC aplicada ao projeto.

## Tecnologias utilizadas

### Back-end

- Python
- Flask
- PostgreSQL
- Psycopg2

### Front-end

- HTML5
- CSS3
- JavaScript

### Ferramentas

- Git
- GitHub
- Visual Studio Code

## Estrutura do projeto

cinereview/
|
|--app.py
|
|--models/
|
   |--conexao.py
   |--resenha_model.py
|
|--templates/
|
   |--index.html
   |--adicionar.html
   |--editar.html
|
|--static/
|
   |--style.css
|
|--Resenhas_DB.sql
|
|--README.md

## Banco de Dados

A principal tabela utilizada pelo sistema é a tabela resenha.

### Estrutura:

CREATE TABLE resenha (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    ano INTEGER NOT NULL,
    resenha TEXT NOT NULL,
    nota INTEGER NOT NULL CHECK (nota BETWEEN 0 AND 10),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

### Campos:

Campo                         Descrição
 id	                Identificador único da resenha
nome	                 Nome do filme ou série
ano	                Ano de lançamento do filme ou série
resenha	                   Texto da avaliação
nota	            Nota atribuída ao filme ou série
data_criacao	        Data de criação da resenha

## Arquitetura MVC

O projeto segue o padrão arquitetural MVC (Model-View-Controller). Atualmente, a camada Controller permanece integrada ao arquivo app.py, enquanto a camada Model está organizada na pasta models e a camada View na pasta templates.

### Model:

Responsável pela comunicação com o banco de dados e manipulação das informações.

#### Exemplo:

models/resenha_model.py

### View:

Responsável pela apresentação das informações ao usuário.

#### Exemplo:

templates/index.html

### Controller:

Responsável pela lógica da aplicação e pelas regras de negócio.

#### Exemplo: 

Ele ainda está integrado ao app.py.

## Interface

O CineReview possui uma interface moderna com:

- Tema escuro
- Cards para exibição das resenhas
- Sistema de busca e filtros
- Organização das informações dos filmes
- Layout responsivo

## Como executar o projeto

### 1. Clone o repositório

git clone https://github.com/ALBERT979-ui/cinereview.git

### 2. Entre na pasta do projeto:

cd .\cinereview\

### 3. Crie um ambiente virtual

#### 3.1 No Windows:

python -m venv venv

#### 3.2 Ative o ambiente virtual

venv\Scripts\activate

#### 3.3 No Linux/Mac:

source venv/bin/activate

### 4. Instale as dependências

pip install -r requirements.txt

### 5. Configure o banco de dados

O projeto utiliza PostgreSQL para armazenar as resenhas.

#### 5.1 Crie um banco de dados chamado:

cine_review

#### 5.2 Depois execute o arquivo:

Resenhas_DB.sql

Esse arquivo contém a criação da tabela utilizada pelo sistema.

### 6. Configure a conexão com o banco

#### 6.1 Configure as informações do PostgreSQL:

Configure essas informações no arquivo models/conexao.py.

host="localhost"
database="cine_review"
user="postgres"
password="postgres"
port="5432"

### 7. Execute a aplicação

#### 7.1 No terminal:

python app.py

A aplicação estará disponível em:

http://127.0.0.1:5000

## Autor

Desenvolvido por:

- Cláudia Oliveira Cândido
- Gabriel Alves Trigueiro
- Jayane da Silva Ferreira
- Nadja Lorena Dantas Toscano

Projeto acadêmico desenvolvido para a disciplina de Programação de Aplicações Web.

## Licença

Este projeto foi desenvolvido com finalidades educacionais por estudantes do Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Norte, no ano de 2026.