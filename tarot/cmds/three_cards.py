import random
import discord
from src.utils import get_three_cards_image
from src.tarot_data import tarot_data

async def three_cards(interaction: discord.Interaction):
    selected_cards = random.sample(tarot_data, 3)
    reversed_flags = [random.random() < 0.2 for _ in range(3)]
    cards_with_flags = list(zip(selected_cards, reversed_flags))

    embed = discord.Embed(
        color=0x9400D3
    )

    positions = ["Past", "Present", "Future"]
    for i, (card, reversed_card) in enumerate(cards_with_flags):
        desc = f"*Reversed:* {card['reversed_meaning']}" if reversed_card and 'reversed_meaning' in card else card['description']
        embed.add_field(name=f"{positions[i]}: {card['name']}", value=desc, inline=False)

    file, filename = get_three_cards_image(cards_with_flags)
    if file:
        embed.set_image(url=f"attachment://{filename}")
        await interaction.response.send_message(embed=embed, file=file)
    else:
        await interaction.response.send_message(embed=embed)