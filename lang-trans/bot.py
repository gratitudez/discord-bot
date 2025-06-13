import discord
from discord.ext import commands
from src.config import TOKEN, COMMAND_PREFIX

# Bot setup with all intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        await bot.load_extension('src.translation')
        print('Successfully loaded translation cog')
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error during setup: {e}")

if __name__ == '__main__':
    if not TOKEN:
        raise ValueError("No Discord token found in .env file")
    bot.run(TOKEN) 