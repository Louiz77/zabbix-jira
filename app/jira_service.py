from jira import JIRA
from .register_log import logger
from config import Config

class JiraService:
    def __init__(self):
        # Configure suas credenciais do Jira e a URL do servidor
        self.jira = JIRA(server="https://itfacil.atlassian.net", basic_auth=(Config.JIRA_API_EMAIL, Config.JIRA_API_TOKEN))

    def create_issue(self, project_key, summary, description, issue_type="Task"):
        try:
            issue = self.jira.create_issue(
                project=project_key,
                summary=summary,
                description=description,
                issuetype={"name": issue_type},
            )
            return issue.key
        except Exception as e:
            logger(f"Erro ao criar issue no Jira: {e}")
            return None

    def get_transitions(self, issue_key):
        try:
            transitions = self.jira.transitions(issue_key)
            print(f"Transições disponíveis para {issue_key}:")
            for transition in transitions:
                print(f"ID: {transition['id']}, Nome: {transition['name']}")
            return transitions
        except Exception as e:
            print(f"Erro ao obter transições para {issue_key}: {e}")

    def transition_issue(self, issue_key, transition_name):
        try:
            # Obter todas as transições disponíveis para a issue
            transitions = self.get_transitions(issue_key)

            # Procurar pela transição que corresponde ao nome
            transition_id = None
            for t in transitions:
                if t['name'].strip().lower() == transition_name.strip().lower():
                    transition_id = t['id']
                    break

            # Validar se a transição foi encontrada
            if not transition_id:
                raise ValueError(f"Transição '{transition_name}' não encontrada para a issue {issue_key}. "
                                 f"Transições disponíveis: {[t['name'] for t in transitions]}")

            # Realizar a transição usando o ID
            self.jira.transition_issue(issue_key, transition_id)
            logger(f"Issue {issue_key} movida com sucesso usando a transição '{transition_name}'")
        except Exception as e:
            logger(f"Erro ao realizar transição no Jira para a issue {issue_key}: {e}")
            raise

