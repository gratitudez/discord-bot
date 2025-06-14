## Prerequisites
- Python 3.8 or higher  
- A Discord bot and its token (create one at [Discord Developer Portal](https://discord.com/developers/applications))
- Make sure to add "bot" scope at the installation section on the Developer Portal

## Tarot Features
- `/one_card` – Single card reading  
- `/three_cards` – Past, present, and future reading  
- `/yes_no` – Yes or no answer to a question

## Lang-Trans Features
- `/languages` – List all supported language + simple guide to use commands  
- `/detect` – Detects the language of the given text  
- `/detecttranslate` – Detects language and translate to selected language 
- `/translate` – Translate text to another language

## Lang-Trans Showcase
![Untitled-2024-09-12-1534 (3)](https://github.com/user-attachments/assets/43ec69dd-7248-4a2f-9082-5fd4523c8eca)

## Step by step installation guide

1. **Clone the repository and navigate to the bot directory:**
   ```bash
   git clone https://github.com/gratitudez/discord-bot.git
   cd discord-bot/tarot / cd discord-bot/lang-trans
2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv .venv
   .venv\Scripts\activate (Windows)
   source .venv/bin/activate (Linux)

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt

4. **Add your bot token to a .env file (tarot/lang-trans):**

   ```bash
   echo DISCORD_TOKEN=your_discord_bot_token_here > .env

5. **Run the bot:**

   ```bash
   python bot.py
