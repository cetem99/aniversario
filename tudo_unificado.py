from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Chave para segurança de sessão

# Função para conectar ao banco de dados
def conecta_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lembrar_aniversarios'
    )

# Exibe a página de cadastro
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
            # Inserindo os dados no banco de dados sem criptografar a senha
            sql = "INSERT INTO usuario (nome, email, data_nascimento, senha) VALUES (%s, %s, %s, %s)"
            valores = (nome, email, data_nascimento, senha)
            cursor.execute(sql, valores)
            conexao.commit()
            print(f"Usuário {nome} cadastrado com sucesso!")

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            conexao.rollback()
            return "Erro ao cadastrar usuário.", 500

        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for('login'))  # Redireciona para a página de login após o cadastro

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
            # Buscar o usuário pelo email
            sql = "SELECT * FROM usuario WHERE email = %s"
            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()

            # Verificar a senha diretamente (sem hash)
            if usuario and usuario['senha'] == senha:
                session['usuario'] = usuario['nome']
                return redirect(url_for('criar_aniversariante'))
            else:
                print("Senha incorreta ou usuário não encontrado")  # Debug: Falha na autenticação
                return "Email ou senha incorretos.", 401

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return "Erro no login.", 500

        finally:
            cursor.close()
            conexao.close()

    return render_template('login.html')

# Página para criar aniversariante (somente para usuários logados)
@app.route('/criar_aniversariante', methods=['GET', 'POST'])
def criar_aniversariante():
    if 'usuario' not in session:
        return redirect(url_for('login'))  # Redireciona para o login se o usuário não estiver logado

    if request.method == 'POST':
        nome = request.form['nome']
        data_aniversario = request.form['data_aniversario']
        email = request.form['email']
        telefone = request.form['telefone']
        notificacao = request.form['escolhas']
        felicitacao = request.form['felicitacoes']

        conexao = conecta_banco()
        cursor = conexao.cursor()

        try:
            # Inserindo o aniversariante no banco de dados
            sql = '''INSERT INTO aniversariantes (nome, data_aniversario, email, telefone, notificacao, felicitacao)
                     VALUES (%s, %s, %s, %s, %s, %s)'''
            valores = (nome, data_aniversario, email, telefone, notificacao, felicitacao)
            cursor.execute(sql, valores)
            conexao.commit()

            print(f"Aniversariante {nome} criado com sucesso!")
            return redirect(url_for('criar_aniversariante'))  # Redireciona após a criação

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return "Erro ao criar aniversariante.", 500

        finally:
            cursor.close()
            conexao.close()

    return render_template('criar_aniversariante.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Remove o usuário da sessão
    return redirect(url_for('login'))  # Redireciona para a página de login

if __name__ == '__main__':
    app.run(debug=True)
