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

@app.route('/')
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
    recipient = request.form['email']
    subject = "Contato carlosaw"
    message_body = request.form['message']

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
    recipient = "carlos_augusto_wallauer@outlook.com"  # E-mail fixo do destinatário
    subject = "from carlosaw: " + request.form['email']
    message_recived = request.form['message']

    msg = Message(subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[recipient])
    msg.body = message_recived

    try:
        mail.send(msg)
        return 'Email enviado com sucesso!'
    except Exception as e:
        app.logger.error('Failed to send email', exc_info=True)
        return str(e), 500  # Retorna a string da exceção e o status 500 para indicar erro no servidor





if __name__ == '__main__':
    app.run(debug=True)
