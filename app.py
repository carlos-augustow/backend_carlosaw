import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/hello/', methods=['GET'])
def hello_world():
    return 'Hello World!'

@app.route('/teste_post/', methods=['POST'])
def teste_post():
    data = request.get_json()  # Obtém o JSON enviado
    m = data.get('mensagem')
    e = data.get('email')
    n = data.get('nome')
    return jsonify({"message": f"Olá {n}, email: {e}, mensagem: {m}"})  # Retorna uma resposta em JSON





@app.route('/send_email/', methods=['POST'])
def send_email():

    data = request.get_json();
    recipient = data.get['email']
    subject = "Contato carlosaw"
    message_body = data.get['message']

    msg = Message(subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[recipient])
    msg.body = message_body

    try:
        mail.send(msg)
        return 'Email enviado com sucesso!!'
    except Exception as e:
        app.logger.error('Failed to send email', exc_info=True)
        return str(e), 500  # Retorna a string da exceção e o status 500 para indicar erro no servidor

@app.route('/send_email_to_me/', methods=['POST'])
def send_email_to_me():
    data = request.get_json()
    
    # Correção: Acessar o método get com parênteses
    subject = "from carlosaw: " + data.get('email', 'sem email')
    name = data.get('name', 'sem nome')
    message_received = data.get('message', 'sem mensagem')

    # Montar o corpo da mensagem
    send_message = f"Nome: {name}\nEmail: {data.get('email')}\nMensagem: {message_received}"

    recipient = "carlos_augusto_wallauer@outlook.com"  # E-mail fixo do destinatário
    
    # Criar a mensagem a ser enviada
    msg = Message(subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[recipient])
    msg.body = send_message

    try:
        mail.send(msg)
        return 'Email enviado com sucesso!'
    except Exception as e:
        app.logger.error('Failed to send email', exc_info=True)
        return str(e), 500  # Retorna a string da exceção e o status 500 para indicar erro no servidor




if __name__ == '__main__':
    app.run(debug=True)
