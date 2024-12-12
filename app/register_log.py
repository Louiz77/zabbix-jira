from datetime import datetime

def logger(message):
    try:
        with open(f"./log/report.log", "a") as my_file:
            my_file.write(f"-{datetime.now()} | {message}\n")
    except Exception as e:
        print(e)