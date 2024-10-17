from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Função para conectar ao banco de dados
def conecta_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lembrar_aniversarios'
    )

# Exibe a página de cadastro
@app.route('/', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

# Rota para criar o usuário
@app.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    # Coleta os dados do formulário
    email = request.form['email']
    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    senha = request.form['senha']

    # Conectando ao banco de dados
    conexao = conecta_banco()
    cursor = conexao.cursor()

    try:
        # Inserindo os dados no banco de dados
        sql = "INSERT INTO usuario (nome, email, data_nascimento, senha) VALUES (%s, %s, %s, %s)"
        valores = (nome, email, data_nascimento, senha)
        cursor.execute(sql, valores)
        
        # Confirmando a inserção dos dados
        conexao.commit()

        print(f"Usuário {nome} cadastrado com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conexao.rollback()  # Desfaz a inserção em caso de erro

    finally:
        # Fechando a conexão com o banco de dados
        cursor.close()
        conexao.close()

    # Redireciona para a página de cadastro após a inserção
    return redirect(url_for('cadastro'))

if __name__ == '__main__':
    app.run(debug=True)
