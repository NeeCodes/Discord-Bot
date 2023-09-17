import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

class Translate(commands.Cog): # inherits from commands.Cog

    def __init__(self, client):
        self.client = client

        # initialise the list of supported languages
        self.language_dict = GoogleTranslator().get_supported_languages(as_dict = True)
        self.language_dict = self.language_dict.items()
        self.language_list = ""

        for key, value in self.language_dict:
            key = key.capitalize()
            self.language_list += f"{key} = {value} \n"

    # to create an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Translate initialised! :D")

    # list of supported languages
    @commands.command(aliases = ['trll', 'trlanglist', 'language_list'])
    async def list_languages(self, ctx):
        language_list_embed = discord.Embed(description = f"{self.language_list}", colour = COLOUR)
        await ctx.send(embed = language_list_embed)

    # translate from the source language to the target language
    @commands.command(aliases = ['tr', 'trans'])
    async def translate(self, ctx, source, target, *, search):
        translation = GoogleTranslator(source = f'{source}', target = f'{target}').translate(f"{search}")
        await ctx.send(f"{translation}")


def setup(client): # connect the cog to the bot
    client.add_cog(Translate(client))



