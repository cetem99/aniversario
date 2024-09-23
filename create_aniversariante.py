from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def criar_aniversariante(nome, data_aniversario, email, telefone, notificacao, felicitacao):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()
    comando = 'INSERT INTO aniversariantes (nome, data_aniversario, email, telefone, notificacao, felicitacao) VALUES (%s, %s, %s, %s, %s, %s)'
    valores = (nome, data_aniversario, email, telefone, notificacao, felicitacao)
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

def deletar_aniversariante(nome):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
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
        password='',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()
    comando = 'SELECT nome, data_aniversario, email, telefone, notificacao, felicitacao FROM aniversariantes'
    cursor.execute(comando)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def editar_aniversariante(nome_atual, novo_nome, nova_data_aniversario, novo_email, novo_telefone, nova_notificacao, nova_felicitacao):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()
    comando = '''
        UPDATE aniversariantes 
        SET nome = %s, data_aniversario = %s, email = %s, telefone = %s, notificacao = %s, felicitacao = %s 
        WHERE nome = %s
    '''
    valores = (novo_nome, nova_data_aniversario, novo_email, novo_telefone, nova_notificacao, nova_felicitacao, nome_atual)
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'criar' in request.form:
            nome = request.form['nome']
            data_aniversario = request.form['data_aniversario']
            email = request.form['email']
            telefone = request.form['telefone']
            notificacao = request.form['escolhas']  # Captura o valor do select "escolhas"
            felicitacao = request.form['felicitacoes']  # Captura a mensagem de felicitações
            criar_aniversariante(nome, data_aniversario, email, telefone, notificacao, felicitacao)
            return "Aniversariante criado com sucesso!"
        elif 'deletar' in request.form:
            nome = request.form['nome_deletar']
            deletar_aniversariante(nome)
            return "Aniversariante deletado com sucesso!"
        
        elif 'editar' in request.form:
            # Código para editar um aniversariante
            nome_atual = request.form['nome_atual']
            novo_nome = request.form['nome']
            nova_data_aniversario = request.form['data_aniversario']
            novo_email = request.form['email']
            novo_telefone = request.form['telefone']
            nova_notificacao = request.form['escolhas']
            nova_felicitacao = request.form['felicitacoes']
            editar_aniversariante(nome_atual, novo_nome, nova_data_aniversario, novo_email, novo_telefone, nova_notificacao, nova_felicitacao)
            return "Aniversariante editado com sucesso!"
    
    aniversariantes = listar_aniversariantes()
    return render_template('Gerenciar.html', aniversariantes=aniversariantes)
        

if __name__ == '__main__':
    app.run(debug=True)
