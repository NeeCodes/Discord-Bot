import discord, requests, json
from discord.ext import commands
from bs4 import BeautifulSoup

class Urban(commands.Cog): # inherits from commands.Cog

    def __init__(self, client):
        self.client = client

        self.api_url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

        self.headers = {
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
            'x-rapidapi-key': "b4b3cc758cmsh5ca9656a5e27ff0p113097jsn92effab425b2"}
        
    # to create an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Urban dictionary initialised! :D")

    def create_embed(data, index, search):
        definition = data['list'][index]['definition']
        author = data['list'][index]['author']
        example = data['list'][index]['example']
        date = data['list'][index]['written_on'][:-14]
        votes = data['list'][index]['thumbs_up']

        embed = discord.Embed(title = f"{search}", colour = COLOUR)

        embed.add_field(name = "Definition", value = f"{definition}", inline = False)
        embed.add_field(name = "Examples", value = f"{example}", inline = False)
        embed.add_field(name = "Date Written", value = f"{date}", inline = True)
        embed.add_field(name = "Author", value = f"{author}", inline = True)
        embed.add_field(name = "Votes", value = f"{votes}", inline = True)
        embed.add_field(name = "Page", value = f"{index + 1}", inline = True)

        return embed
    
    def create_embed_invalid():
        embed = discord.Embed(description = "Sorry, the page you requested wasn't found.", colour = COLOUR)

        return embed

    @commands.command(aliases = ['urbandictionary', 'urban', 'urbandic', 'ud'])
    async def urban_dictionary(self, ctx, *, search):
        try:
            index = 0
            querystring = {"term": f"{search}"}

            search_ud = requests.request("GET", self.api_url, headers = self.headers, params = querystring)
            search_ud = search_ud.json()

            embed = self.create_embed(search_ud, index, search)

            message = await ctx.send(embed = embed)

            await message.add_reaction('⬅') # left arrow
            await message.add_reaction('➡') # right arrow

            while True:
                reaction, user = await self.client.wait_for('reaction_add', check = lambda r, u: u.id == ctx.author.id, timeout = 60)

                if str(reaction.emoji) == '➡':
                    try:
                        index += 1
                        embed = self.create_embed(search_ud, index, search)
                        await message.edit(embed = embed)

                    except:
                        index = -1

                elif str(reaction.emoji) == '⬅':
                    try:
                        if index > 0:
                            index -= 1
                            embed = self.create_embed(search_ud, index, search)
                            await message.edit(embed = embed)

                    except:
                        pass

                else:
                    break
        except:
            await ctx.send(embed = self.create_embed_invalid())


def setup(client): # connect the cog to the bot
    client.add_cog(Urban(client))