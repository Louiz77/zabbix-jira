from datetime import datetime
from config import Config

def logger(message):
    try:
        with open(f"{Config.LOG_FOLDER}report.log", "a") as my_file:
            my_file.write(f"-{datetime.now()} | {message}\n")
    except Exception as e:
        print(e)