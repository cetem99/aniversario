from flask import Flask, request, redirect, url_for, render_template
import #nome do banco de dados


api = Flask(__name__)
api.secret_key = '12345' 

def get_db():
    conectar = mysql.connect(Happy)
    conectar.
    return conectar

def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.exexute('''crate table if not exists Frends(
                   id primary key autoincrement,
                   nome text null
                   )''')
    conectar.commit()
    conectar

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nome = request.from['nome']
        conectar = get_db()
        cur = conectar.cursor()
        cur.execute("INSERT INTO Frends(nome) VALUES (?), (nome)")
        conectar.commit()
        conectar.close()
        return redirect(url_for('formulario'))


if __name__ == '__main__':
    Rundb.run(debug=True)