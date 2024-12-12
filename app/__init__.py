from flask import Flask
from .routes import zabbix_bp
from .whatsapp_service import WhatsappService

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.whatsapp_service = WhatsappService(app.config['WHATSAPP_API_URL'])

    app.register_blueprint(zabbix_bp)

    return app
