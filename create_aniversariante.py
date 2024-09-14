from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def criar_aniversariante(nome, data_aniversario, email, telefone):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()
    comando = 'INSERT INTO aniversariantes (nome, data_aniversario, email, telefone) VALUES (%s, %s, %s, %s)'
    valores = (nome, data_aniversario, email, telefone)
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

def deletar_aniversariante(nome):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()
    comando = 'DELETE FROM aniversariantes WHERE nome = %s'
    cursor.execute(comando, (nome,))
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_aniversariantes():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()
    comando = 'SELECT nome FROM aniversariantes'
    cursor.execute(comando)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'criar' in request.form:
            nome = request.form['nome']
            data_aniversario = request.form['data_aniversario']
            email = request.form['email']
            telefone = request.form['telefone']
            criar_aniversariante(nome, data_aniversario, email, telefone)
            return "Aniversariante criado com sucesso!"
        elif 'deletar' in request.form:
            nome = request.form['nome_deletar']
            deletar_aniversariante(nome)
            return "Aniversariante deletado com sucesso!"
    aniversariantes = listar_aniversariantes()
    return render_template('formulario.html', aniversariantes=aniversariantes)

if __name__ == '__main__':
    app.run(debug=True)
