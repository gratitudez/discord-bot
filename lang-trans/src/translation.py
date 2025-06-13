import discord
from discord import app_commands
from discord.ext import commands
from .utils.language_utils import translate_text, detect_language, get_language_name
from .config import LANGUAGE_CODES, COMMON_LANGUAGES

# Other languages (excluding common languages)
OTHER_LANGUAGES = {
    code: name for code, name in LANGUAGE_CODES.items()
    if code not in COMMON_LANGUAGES
}

class Translation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_language_code(self, lang_input: str) -> str:
        """Convert language input (name or code) to proper language code"""
        # If it's already a valid code, return it
        if lang_input in LANGUAGE_CODES:
            return lang_input
        
        # Try case-insensitive match with language names
        lang_input_lower = lang_input.lower()
        for code, name in LANGUAGE_CODES.items():
            if name.lower() == lang_input_lower:
                return code
            
        # If no match found, return None
        return None

    @app_commands.command(name="translate", description="Translate text to another language")
    @app_commands.describe(
        to_lang="Select a common language or choose 'Other Languages'",
        other_lang="If you selected 'Other Languages', choose a language from here",
        text="The text to translate"
    )
    @app_commands.choices(
        to_lang=[
            *[app_commands.Choice(name=name, value=code) 
              for code, name in sorted(COMMON_LANGUAGES.items(), key=lambda x: x[1])],
            app_commands.Choice(name="📚 Other Languages...", value="other")
        ]
    )
    async def translate(self, interaction: discord.Interaction, to_lang: str, other_lang: str = None, text: str = None):
        await interaction.response.defer(ephemeral=True)

        try:
            target_lang = other_lang if to_lang == "other" else to_lang
            
            if to_lang == "other" and not other_lang:
                await interaction.followup.send(
                    "Please select a language from the 'other_lang' dropdown when choosing 'Other Languages'.",
                    ephemeral=True
                )
                return

            if target_lang.startswith('zh-'):
                target_lang = target_lang.upper()

            result = await translate_text(text, target_lang)
            
            embed = discord.Embed(color=discord.Color.blue())
            embed.add_field(name=f"From {LANGUAGE_CODES.get(result['src'], 'Unknown')}", value=text, inline=False)
            embed.add_field(name=f"To {LANGUAGE_CODES[target_lang]}", value=result['text'], inline=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            await interaction.followup.send(
                "An error occurred during translation. Please try again.",
                ephemeral=True
            )

    @translate.autocomplete('other_lang')
    async def other_lang_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        choices = [
            app_commands.Choice(name=name, value=code)
            for code, name in sorted(OTHER_LANGUAGES.items(), key=lambda x: x[1])
        ]
        
        if not current:
            return choices[:25]
        
        return [
            choice for choice in choices
            if current.lower() in choice.name.lower()
        ][:25]

    @app_commands.command(name="languages", description="List all available languages")
    async def languages(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Available Languages",
            description="Use /translate or /detecttranslate commands with these options:\n\n" +
                      "1. Select from Common Languages in the first dropdown\n" +
                      "2. Or choose '📚 Other Languages...' and use the second dropdown",
            color=discord.Color.green()
        )
        
        common_langs = sorted(COMMON_LANGUAGES.items(), key=lambda x: x[1])
        common_field = "\n".join([f"• {name} ({code})" for code, name in common_langs])
        embed.add_field(name="Common Languages", value=common_field, inline=False)
        
        sorted_other = sorted(OTHER_LANGUAGES.items(), key=lambda x: x[1])
        languages_per_field = 15
        for i in range(0, len(sorted_other), languages_per_field):
            chunk = sorted_other[i:i + languages_per_field]
            field_value = "\n".join([f"• {name} ({code})" for code, name in chunk])
            embed.add_field(name=f"Other Languages - Part {i//languages_per_field + 1}", value=field_value, inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="detecttranslate", description="Detect language and translate to selected language")
    @app_commands.describe(
        to_lang="Select a common language or choose 'Other Languages'",
        other_lang="If you selected 'Other Languages', choose a language from here",
        text="The text to detect and translate"
    )
    @app_commands.choices(
        to_lang=[
            *[app_commands.Choice(name=name, value=code) 
              for code, name in sorted(COMMON_LANGUAGES.items(), key=lambda x: x[1])],
            app_commands.Choice(name="📚 Other Languages...", value="other")
        ]
    )
    async def detecttranslate(self, interaction: discord.Interaction, to_lang: str, other_lang: str = None, text: str = None):
        await interaction.response.defer(ephemeral=True)

        try:
            target_lang = other_lang if to_lang == "other" else to_lang
            
            if to_lang == "other" and not other_lang:
                await interaction.followup.send(
                    "Please select a language from the 'other_lang' dropdown when choosing 'Other Languages'.",
                    ephemeral=True
                )
                return

            if target_lang.startswith('zh-'):
                target_lang = target_lang.upper()

            detected = await detect_language(text)
            result = await translate_text(text, target_lang)
            
            embed = discord.Embed(color=discord.Color.purple())
            embed.add_field(name="Language", value=f"{LANGUAGE_CODES.get(detected, 'Unknown')} ({detected})", inline=False)
            embed.add_field(name="Original", value=text, inline=False)
            embed.add_field(name="Translation", value=result['text'], inline=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            await interaction.followup.send(
                "An error occurred while detecting and translating. Please try again.",
                ephemeral=True
            )

    @detecttranslate.autocomplete('other_lang')
    async def detecttranslate_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        return await self.other_lang_autocomplete(interaction, current)

    @app_commands.command(name="detect", description="Detect the language of the given text")
    @app_commands.describe(text="The text to analyze")
    async def detect(self, interaction: discord.Interaction, text: str):
        try:
            detected = await detect_language(text)
            language_name = get_language_name(detected)
            
            embed = discord.Embed(color=discord.Color.purple())
            embed.add_field(name="Text", value=text, inline=False)
            embed.add_field(name="Language", value=f"{language_name} ({detected})", inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                "An error occurred while detecting the language. Please try again.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Translation(bot)) 