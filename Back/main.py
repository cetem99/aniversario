from flask import Flask, request, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__)
app.secret_key = '12345'

def get_db():
    conectar = mysql.connector.connect(
        host="localhost",
        user="seu_usuario",
        password="sua_senha",
        database="Happy"
    )
    return conectar

def criar_tabela():
    conectar = get_db()
    cursor = conectar.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Frends (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL
        )
    ''')
    conectar.commit()
    conectar.close()

@app.route('/Gerenciar.html', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nome = request.form['nome']
        conectar = get_db()
        cur = conectar.cursor()
        cur.execute("INSERT INTO Frends(nome) VALUES (%s)", (nome,))
        conectar.commit()
        conectar.close()
        return redirect(url_for('formulario'))
    return render_template('Gerenciar.html')  # Referencia o template HTML

if __name__ == '__main__':
    criar_tabela()  # Cria a tabela ao iniciar a aplicação
    app.run(debug=True)
