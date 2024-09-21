# Aplicativo de Lembrete de Aniversários

Este é um aplicativo web simples, desenvolvido com Flask e MySQL, para gerenciar e acompanhar aniversários. Os usuários podem criar, visualizar e excluir entradas de aniversariantes com informações como nome, data de aniversário, e-mail e telefone.

## Funcionalidades

- Adicionar um novo lembrete de aniversário com os seguintes detalhes:
  - Nome
  - Data de Aniversário
  - E-mail
  - Telefone
- Visualizar uma lista de todos os aniversariantes
- Excluir entradas de aniversários

## Tecnologias Utilizadas

- **Backend**: [Flask](https://flask.palletsprojects.com/)
- **Banco de Dados**: [MySQL](https://www.mysql.com/)
- **Frontend**: HTML, CSS (você pode customizar mais ou usar Bootstrap)
- **Template Engine**: Jinja2 (engine de templates padrão do Flask)

## Instalação

### Pré-requisitos

- Python 3.x
- MySQL Server
- Conector MySQL para Python (`mysql-connector-python`)

### Passos

1. Clone o repositório:

    ```bash
    git clone https://github.com/seuusuario/app-lembrete-aniversarios.git
    cd app-lembrete-aniversarios
    ```

2. Configure o ambiente virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate
    ```

3. Instale os pacotes Python necessários:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure o Banco de Dados MySQL:

   - Crie o banco de dados usando o MySQL Workbench ou linha de comando:
     ```sql
     CREATE DATABASE lembrar_aniversarios;
     ```

   - Importe a estrutura da tabela do arquivo `schema.sql`:
     ```bash
     mysql -u root -p lembrar_aniversarios < schema.sql
     ```

5. Configure a conexão com o banco de dados:

   - Atualize os detalhes de conexão no arquivo `app.py` caso necessário:
     ```python
     conexao = mysql.connector.connect(
         host='localhost',
         user='root',
         password='suasenha',
         database='lembrar_aniversarios'
     )
     ```

6. Execute a aplicação:

    ```bash
    flask run
    ```

   O app estará rodando em `http://127.0.0.1:5000`.

## Como Usar

1. Acesse a página inicial: `http://127.0.0.1:5000/lembrar_aniversariante`.
2. Preencha o formulário com o nome, data de aniversário, e-mail e telefone para adicionar um novo aniversariante.
3. Para visualizar e gerenciar os aniversariantes existentes, acesse: `http://127.0.0.1:5000/aniversariantes`.
4. Você pode excluir uma entrada clicando no botão "Excluir" ao lado do registro de um aniversariante.



