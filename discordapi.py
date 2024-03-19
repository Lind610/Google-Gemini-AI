import discord
from discord import app_commands

import os
import gemini

class ChatBot(discord.Client):
    def __init__(self, *, intents, loop=None, gemini_model=gemini.GeminiManager, **options):
        self.Gemini = gemini_model
        super().__init__(intents=intents, loop=loop, **options)

    async def on_message(self, message: discord.Message):
        if message.author.bot:  # Ignores all bot input including itself.
            return

        msg = message.content.split(" ")

        if msg[0] == "Gemini":
            response = self.Gemini.interact(' '.join(msg[1:]))
            await message.channel.send(response)

    async def on_connect(self):
        print("[Discord] Connecting to discord!")

    async def on_ready(self):
        await tree.sync()
        await self.change_presence(activity=discord.Game(name="Ready to rumble"))

        print("[Discord] Bot is ready!")


if __name__ == "__main__":
    # Initalize Gemini client
    Gemini = gemini.GeminiManager()

    # Initalize Discord client
    client = ChatBot(gemini_model=Gemini, intents=discord.Intents.all())
    tree = app_commands.CommandTree(client)

    @tree.command(name="chat", description="Sends messages to the Google Gemini API")
    async def chat(interaction: discord.Interaction, message:str):
        response = Gemini.interact(message)
        await interaction.response.send_message(
            response
        )

    @tree.command(
        name="reset", description="Restarts the chat, wiping the model's history"
    )
    async def reset(interaction: discord.Interaction):
        response = Gemini.reset()
        await interaction.response.send_message("Successfully wiped models history!")

    @tree.command(
        name="personality", description="Changes the models personality based on a inital prompt and performs a reset"
    )
    async def personality(interaction: discord.Interaction, init_prompt: str):
        Gemini.init_msg = init_prompt
        response = Gemini.reset()
        await interaction.response.send_message("Successfully performed the changes!")

    client.run(os.getenv("DISCORD_API_KEY"))
