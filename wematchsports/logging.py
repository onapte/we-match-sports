import datetime

def log_message(message):
    """
    Logs a message with a timestamp.
    :param message: The message to log.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")