from flask import Flask, redirect, url_for, flash, render_template, request, session
import mysql.connector
from mysql.connector import errorcode  # Importa para capturar códigos de erro
from create_aniversariante import create_bp  # Certifique-se que o nome do arquivo está correto

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

        if session['usuario']:
            print("minha senha é: ", senha)
            senha = '123456'
            email= 'gui@gmail.com'
            senha = senha.strip()
        else:
            return "Erro: Senha não pode ser vazia.", 400

        conexao = conecta_banco()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM usuario WHERE email = %s"
            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()

            if usuario and usuario['senha'] == senha:
                session['usuario'] = usuario['nome']
                return redirect(url_for('create_bp.index'))
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


# Rota para logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# Registro do Blueprint do outro arquivo
app.register_blueprint(create_bp, url_prefix='/aniversariante')


if __name__ == '__main__':
    app.run(debug=True)
