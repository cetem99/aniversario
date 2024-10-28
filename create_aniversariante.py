from flask import Blueprint, render_template, request, redirect
import mysql.connector

create_bp = Blueprint('create_bp', __name__)  # Definição correta do Blueprint

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

def obter_aniversariante_por_nome(nome):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lembrar_aniversarios'
    )
    cursor = conexao.cursor()
    comando = 'SELECT nome, data_aniversario, email, telefone, notificacao, felicitacao FROM aniversariantes WHERE nome = %s'
    cursor.execute(comando, (nome,))
    aniversariante = cursor.fetchone()
    cursor.close()
    conexao.close()
    return aniversariante

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

@create_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_aniversario = request.form.get('data_aniversario')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        notificacao = request.form.get('escolhas')
        felicitacao = request.form.get('felicitacoes')

        # Verifica se algum campo é None ou vazio
        if not all([nome, data_aniversario, email, telefone, notificacao, felicitacao]):
            return "Erro: Todos os campos devem ser preenchidos!", 400  # Retorna um erro 400 se algum campo obrigatório não for preenchido

        criar_aniversariante(nome, data_aniversario, email, telefone, notificacao, felicitacao)
        return redirect('/')  # Redireciona para a listagem de aniversariantes
    
    aniversariantes = listar_aniversariantes()
    return render_template('Gerenciar.html', aniversariantes=aniversariantes)

@create_bp.route('/editar', methods=['POST'])
def editar():
    nome_atual = request.form.get('nome_atual')
    aniversariante = obter_aniversariante_por_nome(nome_atual)
    
    if aniversariante is None:
        return "Erro: Aniversariante não encontrado!", 404  # Retorna um erro 404 se o aniversariante não for encontrado

    return render_template('editar.html', aniversariante=aniversariante)

@create_bp.route('/salvar_edicao', methods=['POST'])
def salvar_edicao():
    nome_atual = request.form.get('nome_atual')
    novo_nome = request.form.get('nome')
    nova_data_aniversario = request.form.get('data_aniversario')
    novo_email = request.form.get('email')
    novo_telefone = request.form.get('telefone')
    nova_notificacao = request.form.get('escolhas')
    nova_felicitacao = request.form.get('felicitacoes')

    # Verifica se algum campo é None ou vazio
    if not all([novo_nome, nova_data_aniversario, novo_email, novo_telefone, nova_notificacao, nova_felicitacao]):
        return "Erro: Todos os campos devem ser preenchidos!", 400  # Retorna um erro 400 se algum campo obrigatório não for preenchido

    editar_aniversariante(nome_atual, novo_nome, nova_data_aniversario, novo_email, novo_telefone, nova_notificacao, nova_felicitacao)
    return redirect('/')
