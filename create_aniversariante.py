from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def criar_aniversariante(nome, data_aniversario):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()

    comando = f'INSERT INTO aniversariantes (nome, data_aniversario) VALUES ("{nome}", "{data_aniversario}")'
    cursor.execute(comando)
    conexao.commit()

    cursor.close()
    conexao.close()

@app.route('/lembrar_aniversariante', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        data_aniversario = request.form['data_aniversario']  # Captura a data do formulário
        criar_aniversariante(nome, data_aniversario)
        return "Aniversariante criado com sucesso!"
    else:
        return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)
