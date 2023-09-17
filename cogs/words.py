import discord, requests, json, random
from discord.ext import commands

class Words(commands.Cog): # inherits from commands.Cog

    def __init__(self, client):
        self.client = client

        # calling the dictionary and thesaurus APIs (merriam webster)
        self.dictionary_api = requests.get(
            "https://www.dictionaryapi.com/api/v3/references/collegiate/json/voluminous?key=b91d844a-4cd4-409a-a554-95838acc96ee")
        self.thesaurus_api = requests.get(
            "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/umpire?key=c1cd0752-4d3f-401a-8c1b-3699a6d06a82")

        self.dictionary_api = self.dictionary_api.json()
        self.thesaurus_api = self.thesaurus_api.json()

        # file with a bunch of random words, to be used for the random word definition 
        with open("assets/filtered_words.json") as words_file:
            self.words = json.load(words_file)

    # to create an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Words initialised! :D")

    # want to select parts of this data
    @commands.command(aliases = ['rw', 'word', 'wotd', 'randomword'])
    async def random_word(self, ctx):
        word = random.choice(self.words)

        word_define_url = requests.get(
            f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=b91d844a-4cd4-409a-a554-95838acc96ee")

        word_define_json = word_define_url.json()

        definitions = ""

        for index, definition in enumerate(word_define_json[0]['shortdef'], start = 1):
            definitions += f"{index}] {definition}\n\n "

        definition_embed = discord.Embed(title = f"{word.capitalize()}", description = f"{definitions}", colour=COLOUR)

        await ctx.send(embed = definition_embed)

    @commands.command(aliases = ['def', 'df'])
    async def define(self, ctx, search):
        word_define_url = requests.get(
            f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{search}?key=b91d844a-4cd4-409a-a554-95838acc96ee")

        word_define_json = word_define_url.json()

        definitions = ""

        for index, definition in enumerate(word_define_json[0]['shortdef'], start = 1):
            definitions += f"{index}] {definition}\n\n "

        definition_embed = discord.Embed(title = f"{search.capitalize()}", description = f"{definitions}", colour=COLOUR)

        await ctx.send(embed = definition_embed)


def setup(client): # connect the cog to the bot
    client.add_cog(Words(client))



