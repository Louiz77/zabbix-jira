from flask import Blueprint, request, jsonify, current_app
from .jira_service import JiraService
from .zabbix_service import ZabbixService
import json
import re
from .register_log import logger

zabbix_bp = Blueprint('zabbix', __name__)
zabbix_service = ZabbixService()
zabbix_service.load_mapping_from_file()

jira_service = JiraService()  # Instância do serviço do Jira

def clean_json_string(json_string):
    """
    Limpa e ajusta o JSON bruto recebido do Zabbix.
    """
    json_string = re.sub(r'\s+', ' ', json_string)
    json_string = re.sub(r'("problem":\s*")([^"]*?)"([^"]*?)"([^"]*?")', r'\1\2\3 \4', json_string)
    json_string = re.sub(r'("item_name":\s*")([^"]*?)"([^"]*?)"([^"]*?")', r'\1\2\3 \4', json_string)
    json_string = re.sub(r'("problem":\s*"[^"]+)(,?\s*"host_ip")', r'\1", \2', json_string)
    json_string = re.sub(r'("item_name":\s*"[^"]+)(,?\s*"item_value")', r'\1", \2', json_string)

    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logger(f"Erro ao decodificar JSON: {e}. Retornando JSON bruto.")
        return json_string

@zabbix_bp.route('/zabbix-webhook', methods=['POST'])
def handle_zabbix_webhook():
    try:
        whatsapp_service = current_app.whatsapp_service

        # Receber os dados do Zabbix
        raw_data = request.data.decode('utf-8')
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            data = clean_json_string(raw_data)
            if isinstance(data, str):
                data = json.loads(data)

    except Exception as e:
        logger(f"Falha ao processar dados: {e}")
        return jsonify({'error': 'Falha ao processar dados', 'details': str(e)}), 500

    severity = data.get('severity', '').lower()
    title = data.get('problem', 'Problema sem título').replace('"', '\\"')
    item_value = data.get('item_value', 'Valor atual nao disponivel')
    host_description = data.get('host_description', 'Descricao nao disponivel')

    description = (
        f"🚨 *ALERTA DE PROBLEMA* 🚨\n\n"
        f"⚠️ *Status*: {data.get('trigger_status', 'Status não disponível')}\n"
        f"🔧 *Titulo do Problema*: _{title}_\n"
        f"📈 *Valor Atual*: _{item_value}_\n"
        f"🖥️ *Host*: {data.get('host', 'Host não disponível')}\n"
        f"🌐 *IP*: {data.get('host_ip', 'IP não disponível')}\n"
        f"🏷️ *Descricao da Maquina*: _{host_description}_\n"
        f"📊 *Severidade*: {data.get('severity', 'Severidade não disponível')}\n"
    )

    # logica para detectar severidade
    if severity in ['high', 'disaster']:
        project_key = "EE"  # projeto do jira
        issue_key = jira_service.create_issue(project_key, title, description)

        if not issue_key:
            logger('Falha ao criar issue no Jira')
            return jsonify({'error': 'Falha ao criar issue no Jira'}), 500

        zabbix_service.save_card_mapping(data.get('trigger_id'), issue_key)

        # issue criada no jira
        logger(f"Issue criada no Jira: {issue_key}")

    elif severity == 'average':
        # severidade average detectada
        logger("Severidade média detectada, nenhuma issue será criada no Jira.")

    else:
        # caso a severidade recebida nao esteja no escopo de problemas
        logger(f"Severidade '{severity}' não é considerada para ações.")

    # sendMessage
    session_id = "undefined"
    try:
        whatsapp_service.sendMessage(description, session_id)
        logger("Mensagem enviada no WhatsApp com sucesso.")
    except Exception as e:
        logger(f"Erro ao enviar mensagem no WhatsApp: {e}")

    logger('Processamento concluído com sucesso')
    return jsonify({'message': 'Processamento concluído com sucesso'}), 200

@zabbix_bp.route('/zabbix-resolved', methods=['POST'])
def handle_zabbix_resolved():
    try:
        whatsapp_service = current_app.whatsapp_service

        # recebendo os dados do zabbix
        raw_data = request.data.decode('utf-8')
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            data = clean_json_string(raw_data)
            if isinstance(data, str):
                data = json.loads(data)

    except Exception as e:
        logger(f'Falha ao processar dados: {e}')
        return jsonify({'error': 'Falha ao processar dados', 'details': str(e)}), 500

    trigger_id = data.get('trigger_id')
    host = data.get('host', 'Host não disponível')
    problem_title = data.get('problem', 'Problema não especificado')
    issue_key = zabbix_service.get_card_id_by_trigger(trigger_id)

    # base da mensagem
    message = (
        f"✅ *PROBLEMA RESOLVIDO!* ✅\n\n"
        f"🔧 *Título do Problema*: _{problem_title}_\n"
        f"🖥️ *Host*: _{host}_\n"
        f"📍 *Trigger ID*: {trigger_id}\n"
    )

    # mover para concluido
    if issue_key:
        try:
            jira_service.transition_issue(issue_key, "Marcar como Concluído")
            logger(f"Issue {issue_key} movida para 'Concluído'.")
        except Exception as e:
            logger(f'Falha ao mover issue no Jira: {e}')
            return jsonify({'error': 'Falha ao mover issue no Jira', 'details': str(e)}), 500
    else:
        logger(f"Trigger ID {trigger_id} não possui issue correspondente no Jira. Nenhuma transição realizada.")

    # sendMessage
    session_id = "undefined"
    try:
        whatsapp_service.sendMessageResolved(message, session_id)
        logger("Mensagem de resolução enviada no WhatsApp com sucesso.")
    except Exception as e:
        logger(f"Erro ao enviar mensagem no WhatsApp: {e}")

    logger("Processamento de resolução concluído com sucesso")
    return jsonify({'message': 'Processamento de resolução concluído com sucesso'}), 200


