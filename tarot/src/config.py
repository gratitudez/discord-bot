from dotenv import load_dotenv
import os

load_dotenv()

TAROT_CARDS_FOLDER = 'img'
BOT_TOKEN = os.getenv("DISCORD_TOKEN")