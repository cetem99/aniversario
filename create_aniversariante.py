from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)


# Configurar a conexão com o banco de dados MySQL
db_config = {
   'host': 'localhost',
   'user': 'root',  # seu usuário MySQL
   'password': 'sua_senha',  # sua senha MySQL
   'database': 'aniversariante_db'
}


def get_db_connection():
   conn = mysql.connector.connect(**db_config)
   return conn


@app.route('/aniversariantes', methods=['POST'])
def create_aniversariante():
   data = request.get_json()
   nome = data.get('nome')


   if not nome:
       return jsonify({'message': 'Nome é obrigatório'}), 400


   conn = get_db_connection()
   cursor = conn.cursor()
   query = 'INSERT INTO aniversariante (nome) VALUES (%s)'
   cursor.execute(query, (nome,))
   conn.commit()
   cursor.close()
   conn.close()


   return jsonify({'message': 'Aniversariante criado com sucesso', 'nome': nome}), 201


if __name__ == '__main__':
   app.run(port=5000,debug=True)
