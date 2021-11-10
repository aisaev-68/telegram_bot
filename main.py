import os
import time
from botrequests import cert
from dotenv import load_dotenv
import telebot
import logging
import cherrypy
from pyngrok import ngrok


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


WEBHOOK_LISTEN = "127.0.0.1"
WEBHOOK_PORT = 443

TOKEN = os.environ.get('TELEGRAM_API_TOKEN')

NGTOKEN = os.environ.get('TOKEN_NGROK')
ngrok.set_auth_token(NGTOKEN)
ngrok.connect()
ngrok.set_auth_token(NGTOKEN)
ngrok_tunnels = ngrok.get_tunnels()

WEBHOOK_HOST = ngrok_tunnels[0].public_url
WEBHOOK_URL_BASE = "%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)

# Создает сертификат для сгенерированного адреса
cert.create_cert(WEBHOOK_HOST)

WEBHOOK_SSL_CERT = "webhook_cert.pem"
WEBHOOK_SSL_PRIV = "webhook_pkey.pem"

bot = telebot.TeleBot(TOKEN, parse_mode=None)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# WebhookServer
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Привет, Я эхобот.\n"
                  "Я здесь, чтобы повторить вам ваши добрые слова."))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

bot.remove_webhook()
time.sleep(3)
w = bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))
if w:
    print('webhook setup ok')
else:
    print('webhook setup failed')

# Отключение журнала CherryPy
access_log = cherrypy.log.access_log
for handler in tuple(access_log.handlers):
    access_log.removeHandler(handler)

# Запуск сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})