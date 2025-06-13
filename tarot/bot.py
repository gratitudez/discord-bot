import discord
from discord import app_commands
from src.config import BOT_TOKEN
from cmds import one_card, three_cards, yes_no

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await tree.sync()
    print("Commands synced!")

# Register commands with the tree
@tree.command(name="one_card", description="Draw a single tarot card for guidance")
async def _one_card(interaction: discord.Interaction):
    await one_card(interaction)

@tree.command(name="three_cards", description="Draw three tarot cards for a past-present-future reading")
async def _three_cards(interaction: discord.Interaction):
    await three_cards(interaction)

@tree.command(name="yes_no", description="Ask a yes/no question and receive guidance from the tarot")
async def _yes_no(interaction: discord.Interaction, question: str):
    await yes_no(interaction, question)

client.run(BOT_TOKEN)