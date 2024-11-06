from flask import Flask
import mysql.connector
from datetime import datetime, timedelta, date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import threading
import time

# Configuração do Flask
app = Flask(__name__)

# Função para conectar ao banco de dados MySQL usando mysql.connector
def conectar_bd():
    return mysql.connector.connect(
        host='localhost',
        user='root',        # Substitua pelo seu usuário
        password='12345678',      # Substitua pela sua senha
        database='lembrar_aniversarios'
    )

# Função para calcular a data de notificação com base na escolha do usuário
def calcular_data_notificacao(data_aniversario, notificacao):
    if notificacao == "No Dia":
        return data_aniversario
    elif notificacao == "1 Dia":
        return data_aniversario - timedelta(days=1)
    elif notificacao == "1 Semana":
        return data_aniversario - timedelta(weeks=1)
    elif notificacao == "2 Semanas":
        return data_aniversario - timedelta(weeks=2)
    elif notificacao == "3 Semanas":
        return data_aniversario - timedelta(weeks=3)
    elif notificacao == "1 mes":
        return data_aniversario - timedelta(days=30)
    return None

# Função para enviar e-mail
def send_email(receiver_email, nome, notificacao):
    sender_email = "guilherme.padilha@sempreceub.com"
    password = "Gui@220803"
    
    subject = f"Aniversário de: {nome}"
    
    if notificacao == "No Dia":
        body = f"🎉 Hoje é o grande dia! {nome} está comemorando o aniversário! 🎂🎈 Não esqueça de enviar seus parabéns! 🥳"
    else:
        body = f"🎉 Falta {notificacao} para o aniversário de {nome}! 🎂🎈 Prepare-se para celebrar e enviar seus parabéns! 🥳"


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"E-mail enviado para {receiver_email}")

# Função que verifica quem deve receber o e-mail de acordo com as datas e preferências
def verificar_aniversarios_para_envio():
    hoje = datetime.now().date()
    conexao = conectar_bd()
    
    try:
        with conexao.cursor() as cursor:
            # Consulta para obter todos os aniversariantes
            cursor.execute("SELECT nome, data_aniversario, email, notificacao FROM aniversariantes")
            aniversariantes = cursor.fetchall()

            # Itera sobre cada aniversariante para verificar a data de envio
            for aniversariante in aniversariantes:
                nome, data_aniversario, email, notificacao = aniversariante
                
                data_notificacao = calcular_data_notificacao(data_aniversario, notificacao)
                
                if data_notificacao and data_notificacao.month == hoje.month and data_notificacao.day == hoje.day:
                    send_email(email, nome, notificacao)
    
    finally:
        conexao.close()

# Agendar o envio de e-mails diariamente
def schedule_emails():
    while True:
        verificar_aniversarios_para_envio()  # Chama a função de envio diretamente
        time.sleep(60 * 60)

# Iniciar o agendamento em segundo plano
threading.Thread(target=schedule_emails).start()

# Rota principal do site Flask
@app.route('/')
def home():
    return "Site funcionando!"

# Inicialização do Flask
if __name__ == "__main__":
    app.run(debug=True)
