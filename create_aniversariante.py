from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def criar_aniversariante(nome):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='aniversario'
    )
    cursor = conexao.cursor()

    comando = f'INSERT INTO aniversariantes (nome) VALUES ("{nome}")' 
    cursor.execute(comando)
    conexao.commit()

    cursor.close()
    conexao.close()

@app.route('/aniversariante', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        criar_aniversariante(nome)
        return "Aniversariante criado com sucesso!"
    else:
        return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)