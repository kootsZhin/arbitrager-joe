import logging
import os
from logging.handlers import TimedRotatingFileHandler

import requests
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_chat_id = os.getenv("CHAT_ID")

def setup_custom_logger(name):
    print(f"Setting up logger {name}...")
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def ping_telegram(msg):
    return requests.post(f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}&text={msg}")
