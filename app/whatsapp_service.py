from flask import jsonify
import requests
import json
from .register_log import logger

class WhatsappService:
    def __init__(self, api_url):
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json"
        }
    def sendMessage(self, message, session_id):
        payload = json.dumps({
            "sessionId": session_id,
            "to": "120363339322672895@g.us",
            "message": str(message)
        })
        print(payload)

        response = requests.request("POST", self.api_url, headers=self.headers, data=payload)
        print(response)
        print(response.status_code)
        print(response.json())
        return jsonify({'message': 'Finalizado'}), 200

    def sendMessageResolved(self, message, session_id):
        payload = json.dumps({
            "sessionId": session_id,
            "to": "120363339322672895@g.us",
            "message": str(message)
        })

        response = requests.request("POST", self.api_url, headers=self.headers, data=payload)

        # Logs detalhados da resposta
        logger(f"Resposta HTTP: {response.text}")
        print(f"Status Code: {response.status_code}")

        # Validar o status HTTP
        if response.status_code != 200:
            logger(f"Erro na API do WhatsApp: {response.status_code} - {response.text}")
            return jsonify({'error': 'Erro na API do WhatsApp'}), response.status_code

        try:
            response_json = response.json()
            print(f"Resposta JSON: {response_json}")
        except json.JSONDecodeError:
            response_json = None

        return jsonify({'message': 'Finalizado', 'response': response_json}), 200

