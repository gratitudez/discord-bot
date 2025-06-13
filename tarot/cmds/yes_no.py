import random
import discord
from src.utils import get_card_color, get_card_image
from src.tarot_data import tarot_data

async def yes_no(interaction: discord.Interaction, question: str):
    card = random.choice(tarot_data)
    reversed_card = random.random() < 0.2
    if 'yes_no' in card:
        if reversed_card:
            answer = "NO" if card['yes_no'].upper() == "YES" else "YES" if card['yes_no'].upper() == "NO" else "MAYBE"
        else:
            answer = card['yes_no'].upper()
    else:
        answer = "MAYBE"

    meaning = card['reversed_meaning'] if reversed_card and 'reversed_meaning' in card else card['description']
    position = "Reversed" if reversed_card else "Upright"

    embed = discord.Embed(
        title=question,
        description=f"The answer is: **{answer}**",
        color=get_card_color(card)
    )

    embed.add_field(name="Card Drawn", value=f"{card['name']} ({position})", inline=False)
    embed.add_field(name="Card Meaning", value=meaning, inline=False)

    image_file, filename = get_card_image(card['name'], card['type'], reversed_card)
    if image_file:
        embed.set_thumbnail(url=f"attachment://{filename}")
        await interaction.response.send_message(embed=embed, file=image_file)
    else:
        await interaction.response.send_message(embed=embed)
