from flask import Blueprint, render_template, request, redirect
import mysql.connector

create_bp = Blueprint('create_bp', __name__)

def criar_aniversariante(nome, data_aniversario, email, telefone, notificacao, felicitacao, usuario_id):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()
    comando = '''
        INSERT INTO aniversariantes (nome, data_aniversario, email, telefone, notificacao, felicitacao, usuario_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    valores = (nome, data_aniversario, email, telefone, notificacao, felicitacao, usuario_id)
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
        password='12345678',
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

def obter_aniversariante_por_nome(nome):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()
    comando = 'SELECT nome, data_aniversario, email, telefone, notificacao, felicitacao FROM aniversariantes WHERE nome = %s'
    cursor.execute(comando, (nome,))
    aniversariante = cursor.fetchone()
    cursor.close()
    conexao.close()
    return aniversariante

@create_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'criar' in request.form:
            nome = request.form['nome']
            data_aniversario = request.form['data_aniversario']  # Formato: YYYY-MM-DD
            email = request.form['email']
            telefone = request.form['telefone']
            notificacao = request.form['escolhas']
            felicitacao = request.form['felicitacoes']
            
            # Supondo que o usuario_id está disponível na sessão ou é enviado no formulário
            usuario_id = request.form['usuario_id']  # Altere conforme necessário
            
            criar_aniversariante(nome, data_aniversario, email, telefone, notificacao, felicitacao, usuario_id)
            return redirect('/')  # Redireciona após a criação
        
        elif 'nome_deletar' in request.form:
            nome = request.form['nome_deletar']
            deletar_aniversariante(nome)
            return redirect('/')  # Redireciona após a exclusão
    
    aniversariantes = listar_aniversariantes()
    return render_template('Gerenciar.html', aniversariantes=aniversariantes)

@create_bp.route('/editar', methods=['POST'])
def editar():
    nome_atual = request.form['nome_atual']
    aniversariante = obter_aniversariante_por_nome(nome_atual)
    return render_template('editar.html', aniversariante=aniversariante)

@create_bp.route('/salvar_edicao', methods=['POST'])
def salvar_edicao():
    try:
        nome_atual = request.form['nome_atual']
        novo_nome = request.form['nome']
        nova_data_aniversario = request.form['data_aniversario']
        novo_email = request.form['email']
        novo_telefone = request.form['telefone']
        nova_notificacao = request.form['escolhas']
        nova_felicitacao = request.form['felicitacoes']
        
        # Imprimindo dados para verificação
        print(f"Editando: {nome_atual} para {novo_nome}")

        editar_aniversariante(nome_atual, novo_nome, nova_data_aniversario, novo_email, novo_telefone, nova_notificacao, nova_felicitacao)
        return redirect('/')  # Redireciona após salvar a edição
    except Exception as e:
        print(f"Erro ao salvar edição: {e}")
        return "Houve um erro ao salvar a edição.", 500

if __name__ == '__main__':
    create_bp.run(debug=True)
