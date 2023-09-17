import discord, requests, wikipedia
from discord.ext import commands
from bs4 import BeautifulSoup

class Wiki(commands.Cog): # inherits from commands.Cog

    def __init__(self, client):
        self.client = client

    # to create an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Wiki initialised! :D")

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

    # useless wiki command (using the wikipedia API)
    @commands.command(aliases = ['uw', 'uselesswiki'])
    async def useless_wiki(self, ctx, *, search):
        try:
            wiki_summary = wikipedia.summary(f"{search}")
            await ctx.send(f"{wiki_summary}")

        except wikipedia.exceptions.DisambiguationError as error:
            options = error.options

            response_text = "Which one of these were you looking for? \n"

            for index, option in enumerate(options):
                response_text += f"{index}) {option} \n"
                
            response_text += "Please type the number corresponding to the article you were looking for: \n"
            await ctx.send(response_text)

            user_choice = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
            user_choice = int(user_choice.content)

            await ctx.send(f"{wikipedia.summary(options[user_choice])}")

        except:
            await ctx.send("I give up :(")

    # actually useful wiki command (WIP)
    @commands.command()
    async def wiki(self, ctx, *, search):
        search.replace(" ", "+") # to fit the format of the google search url

        search_url = requests.get(f"https://www.google.com/search?q=wikipedia+{search}")
        search_soup = BeautifulSoup(search_url.text, "html.parser") # parse the webpage data

        all_links = search_soup.find_all('a')
        all_links = [link.get('href') for link in all_links]

        for link in all_links:
            if 'https://en.wikipedia.org/wiki/' in str(link):
                requested_link = link
                break

        requested_link = requested_link.replace("/url?q=", "")
        requested_link = requested_link.split("&")

        requested_wiki = requested_link[0]

        await ctx.send(f"{requested_wiki}")


def setup(client): # connect the cog to the bot
    client.add_cog(Wiki(client))



