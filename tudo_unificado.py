from flask import Flask, redirect, url_for, flash, render_template, request, session
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Chave de segurança para sessão

# Função para conectar ao banco de dados
def conecta_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='lembrar_aniversarios'
    )

# Exibe a página de cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        senha = request.form['senha']

        conexao = conecta_banco()
        cursor = conexao.cursor()

        try:
            sql = "INSERT INTO usuario (nome, email, data_nascimento, senha) VALUES (%s, %s, %s, %s)"
            valores = (nome, email, data_nascimento, senha)
            cursor.execute(sql, valores)
            conexao.commit()

            # Mensagem de sucesso após cadastro
            flash("Cadastrado com sucesso! Agora, insira seu e-mail e senha para acessar sua conta.", "success")

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            conexao.rollback()

            # Verifica se o erro é de duplicata de chave
            if err.errno == errorcode.ER_DUP_ENTRY:
                flash("Já existe este email cadastrado. Tente novamente com um email diferente.", "error")
            else:
                flash("Erro ao cadastrar usuário. Tente novamente.", "error")
            return redirect(url_for('cadastro'))

        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for('login'))

    return render_template('cadastro.html')

# Exibe a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        conexao = conecta_banco()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM usuario WHERE email = %s"
            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()

            if usuario and usuario['senha'] == senha:
                session['usuario'] = usuario['email']
                return redirect(url_for('criar_aniversariante'))
            else:
                flash("Email ou senha incorretos.", "error")
                return redirect(url_for('login'))

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return "Erro no login.", 500

        finally:
            cursor.close()
            conexao.close()

    return render_template('login.html')

# Rota para criar e listar aniversariantes
@app.route('/criar_aniversariante', methods=['GET', 'POST'])
def criar_aniversariante():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conexao = conecta_banco()
    cursor = conexao.cursor(dictionary=True)

    aniversariantes = []

    if request.method == 'POST':
        # Criação de um novo aniversariante
        nome_aniversariante = request.form['nome_aniversariante']
        data_aniversario = request.form['data_aniversario']
        telefone = request.form['telefone']
        notificacao = request.form['notificacao']
        felicitacao = request.form['felicitacao']
        email_usuario = session['usuario']  # Usando o nome do usuário da sessão

        try:
            sql = """
                INSERT INTO aniversariantes (nome, data_aniversario, email, telefone, notificacao, felicitacao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (nome_aniversariante, data_aniversario, email_usuario, telefone, notificacao, felicitacao)
            cursor.execute(sql, valores)
            conexao.commit()
            flash("Aniversariante criado com sucesso!", "success")
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            conexao.rollback()
            flash("Erro ao criar aniversariante. Tente novamente.", "error")

    # Consulta a lista de aniversariantes do usuário logado
    email_usuario = session['usuario']
    sql = "SELECT * FROM aniversariantes WHERE email = %s"
    cursor.execute(sql, (email_usuario,))
    aniversariantes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template('criar_aniversariante.html', aniversariantes=aniversariantes)

@app.route('/deletar_aniversariante/<int:id>', methods=['GET'])
def deletar_aniversariante(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conexao = conecta_banco()
    cursor = conexao.cursor()

    try:
        sql = "DELETE FROM aniversariantes WHERE id = %s"
        cursor.execute(sql, (id,))
        conexao.commit()
        flash("Aniversariante deletado com sucesso!", "success")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conexao.rollback()
        flash("Erro ao deletar aniversariante. Tente novamente.", "error")
    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for('criar_aniversariante'))
@app.route('/editar_aniversariante/<int:id>', methods=['GET', 'POST'])
def editar_aniversariante(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conexao = conecta_banco()
    cursor = conexao.cursor(dictionary=True)

    if request.method == 'POST':
        # Obtendo os dados do formulário
        nome_aniversariante = request.form['nome_aniversariante']
        data_aniversario = request.form['data_aniversario']
        telefone = request.form['telefone']
        notificacao = request.form['notificacao']
        felicitacao = request.form['felicitacao']

        try:
            # Atualizando o aniversariante no banco de dados
            sql = """
                UPDATE aniversariantes 
                SET nome = %s, data_aniversario = %s, telefone = %s, notificacao = %s, felicitacao = %s
                WHERE id = %s
            """
            valores = (nome_aniversariante, data_aniversario, telefone, notificacao, felicitacao, id)
            cursor.execute(sql, valores)
            conexao.commit()
            flash("Aniversariante atualizado com sucesso!", "success")
            return redirect(url_for('criar_aniversariante'))

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            conexao.rollback()
            flash("Erro ao editar aniversariante. Tente novamente.", "error")

    # Consultando os dados do aniversariante para preencher o formulário
    sql = "SELECT * FROM aniversariantes WHERE id = %s"
    cursor.execute(sql, (id,))
    aniversariante = cursor.fetchone()

    cursor.close()
    conexao.close()

    if aniversariante is None:
        flash("Aniversariante não encontrado!", "error")
        return redirect(url_for('criar_aniversariante'))

    return render_template('editar_aniversariante.html', aniversariante=aniversariante)
@app.route('/sair')
def sair():
    session.pop('usuario', None)  # Remove o usuário da sessão
    flash("Você saiu com sucesso.", "info")  # Mensagem de feedback
    return redirect(url_for('login'))  # Redireciona para a página de login

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
