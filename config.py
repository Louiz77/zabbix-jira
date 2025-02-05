import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
    JIRA_API_EMAIL = os.getenv('JIRA_API_EMAIL')
    WHATSAPP_API_URL = 'http://127.0.0.1:7000/send-message'
    LOG_FOLDER = os.getenv('LOG_FOLDER')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    SMTP_EMAIL = os.getenv('SMTP_EMAIL')