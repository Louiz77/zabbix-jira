from flask import jsonify
import requests
import json
from datetime import datetime

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
        with open("report.log", "a") as my_file:
            my_file.write(f"-{datetime.now()} | Resposta HTTP: {response.text}\n")
        print(f"Status Code: {response.status_code}")

        # Validar o status HTTP
        if response.status_code != 200:
            with open("report.log", "a") as my_file:
                my_file.write(f"-{datetime.now()} | Erro na API do WhatsApp: {response.status_code} - {response.text}\n")

            return jsonify({'error': 'Erro na API do WhatsApp'}), response.status_code

        try:
            response_json = response.json()
            print(f"Resposta JSON: {response_json}")
        except json.JSONDecodeError:
            response_json = None

        return jsonify({'message': 'Finalizado', 'response': response_json}), 200

