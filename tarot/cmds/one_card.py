import random
import discord
from src.utils import get_card_color, get_card_image
from src.tarot_data import tarot_data

async def one_card(interaction: discord.Interaction):
    card = random.choice(tarot_data)
    reversed_card = random.random() < 0.2

    embed = discord.Embed(
        title=card['name'],
        description=card['description'] if not reversed_card else f"*Reversed:* {card.get('reversed_meaning', 'No reversed meaning available.')}",
        color=get_card_color(card)
    )

    for field in ['element', 'zodiac', 'astrological', 'chakra']:
        if field in card:
            embed.add_field(name=field.capitalize(), value=card[field], inline=True)

    embed.add_field(name="Card Position", value="Reversed" if reversed_card else "Upright", inline=False)

    image_file, filename = get_card_image(card['name'], card['type'], reversed_card)
    if image_file:
        embed.set_image(url=f"attachment://{filename}")
        await interaction.response.send_message(embed=embed, file=image_file)
    else:
        await interaction.response.send_message(embed=embed)
