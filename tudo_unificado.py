from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector
from create_aniversariante import create_bp  # Certifique-se que o nome do arquivo está correto

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Chave de segurança para sessão

# Função para conectar ao banco de dados
def conecta_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
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

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            conexao.rollback()
            return "Erro ao cadastrar usuário.", 500

        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for('login'))

    return render_template('cadastro.html')

# Exibe a página de login
@app.route('/', methods=['GET', 'POST'])
# Exibe a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Verifique se a senha não é None antes de aplicar strip
        if senha is not None:
            senha = senha.strip()
        else:
            return "Erro: Senha não pode ser vazia.", 400  # Retorna um erro 400 se a senha não for fornecida

        conexao = conecta_banco()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM usuario WHERE email = %s"
            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()

            if usuario and usuario['senha'] == senha:
                session['usuario'] = usuario['nome']
                return redirect(url_for('create_bp.index'))  # Redireciona para o Blueprint

            else:
                return "Email ou senha incorretos.", 401

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
