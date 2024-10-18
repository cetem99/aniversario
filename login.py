from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessoes'

# Função para conectar ao banco de dados
def conecta_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lembrar_aniversarios'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Conectar ao banco de dados
        conexao = conecta_banco()
        cursor = conexao.cursor(dictionary=True)

        # Verificar se o email e a senha correspondem a algum usuário
        consulta = "SELECT * FROM usuario WHERE email = %s AND senha = %s"
        cursor.execute(consulta, (email, senha))
        usuario = cursor.fetchone()

        # Fechar a conexão com o banco de dados
        cursor.close()
        conexao.close()

        if usuario:
            # Se o login for bem-sucedido, salvar o usuário na sessão
            session['usuario'] = usuario['email']
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return f'Bem-vindo, {session["usuario"]}!'
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
