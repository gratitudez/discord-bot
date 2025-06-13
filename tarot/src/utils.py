import os
import io
from PIL import Image
import discord
from src.config import TAROT_CARDS_FOLDER

def get_card_color(card):
    if 'type' in card:
        card_type = card['type'].lower()
        if 'major arcana' in card_type:
            return 0x9400D3
        elif 'cups' in card_type:
            return 0x0000FF
        elif 'wands' in card_type:
            return 0xFF0000
        elif 'swords' in card_type:
            return 0xFFFF00
        elif 'pentacles' in card_type:
            return 0x00FF00
    return 0x808080

def find_card_image(card_name, card_type):
    if not os.path.exists(TAROT_CARDS_FOLDER):
        os.makedirs(TAROT_CARDS_FOLDER)
        print(f"Created {TAROT_CARDS_FOLDER} folder. Please place your tarot card images there.")
        return None
    
    if card_type == "Major Arcana":
        major_arcana_map = {
            "The Fool": "00", "The Magician": "01", "The High Priestess": "02",
            "The Empress": "03", "The Emperor": "04", "The Hierophant": "05",
            "The Lovers": "06", "The Chariot": "07", "Strength": "08",
            "The Hermit": "09", "Wheel of Fortune": "10", "Justice": "11",
            "The Hanged Man": "12", "Death": "13", "Temperance": "14",
            "The Devil": "15", "The Tower": "16", "The Star": "17",
            "The Moon": "18", "The Sun": "19", "Judgement": "20", "The World": "21"
        }
        card_number = major_arcana_map.get(card_name, "")
        if card_number:
            filename = f"{card_number}-{card_name.replace(' ', '')}.png"
            filepath = os.path.join(TAROT_CARDS_FOLDER, filename)
            if os.path.exists(filepath):
                return filepath
    else:
        suit = card_type
        rank_map = {
            "Ace": "01", "Two": "02", "Three": "03", "Four": "04",
            "Five": "05", "Six": "06", "Seven": "07", "Eight": "08",
            "Nine": "09", "Ten": "10", "Page": "11", "Knight": "12",
            "Queen": "13", "King": "14"
        }
        rank_word = card_name.split(" of ")[0]
        rank_number = rank_map.get(rank_word, "")
        if rank_number:
            filename = f"{suit}{rank_number}.png"
            filepath = os.path.join(TAROT_CARDS_FOLDER, filename)
            if os.path.exists(filepath):
                return filepath

    card_name_clean = card_name.lower().replace(" ", "").replace("the", "")
    for file in os.listdir(TAROT_CARDS_FOLDER):
        if file.lower().endswith('.png') and card_name_clean in file.lower():
            return os.path.join(TAROT_CARDS_FOLDER, file)
    return None

def get_card_image(card_name, card_type, reversed_card=False):
    image_path = find_card_image(card_name, card_type)
    if not image_path or not os.path.exists(image_path):
        return None, None

    if not reversed_card:
        return discord.File(image_path), os.path.basename(image_path)

    try:
        with Image.open(image_path) as img:
            rotated_img = img.rotate(180)
            img_bytes = io.BytesIO()
            rotated_img.save(img_bytes, format=img.format)
            img_bytes.seek(0)
            filename = f"reversed_{os.path.basename(image_path)}"
            return discord.File(img_bytes, filename=filename), filename
    except Exception as e:
        print(f"Error occurred rotating: {e}")
        return discord.File(image_path), os.path.basename(image_path)


def get_three_cards_image(cards):
    images = []
    for card, reversed_card in cards:
        image_path = find_card_image(card['name'], card['type'])
        if not image_path or not os.path.exists(image_path):
            continue

        with Image.open(image_path) as img:
            if reversed_card:
                img = img.rotate(180)
            images.append(img.copy())

    if not images:
        return None, None

    widths, heights = zip(*(img.size for img in images))
    total_width = sum(widths)
    max_height = max(heights)

    combined_image = Image.new("RGB", (total_width, max_height))

    x_offset = 0
    for img in images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.width

    output_buffer = io.BytesIO()
    combined_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    filename = "three_cards.png"
    file = discord.File(output_buffer, filename=filename)
    return file, filename