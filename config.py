import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
    JIRA_API_EMAIL = os.getenv('JIRA_API_EMAIL')
    WHATSAPP_API_URL = 'http://127.0.0.1:7000/send-message'
