from flask import Flask
import #nome do banco de dados


api = Flask(__name__)
api.secret_key = '12345' 

def conectar_db():
    conectar = 
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