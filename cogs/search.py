import discord, requests
from discord.ext import commands
from bs4 import BeautifulSoup

class Search(commands.Cog): # inherits from commands.Cog

    def __init__(self, client):
        self.client = client

    # to create an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Search initialised! :D")

    # search for the weather in an area
    @commands.command(aliases = ['temp', 'temperature'])
    async def weather(self, ctx, *, search):
        search.replace(" ", "+") # to fit the format of the google search url

        search_url = requests.get(f"https://www.google.com/search?q=weather+in+{search}")
        search_soup = BeautifulSoup(search_url.text, "html.parser") # parse the webpage data

        temperature = search_soup.find("span", id='wob_tm').text # find the featured info (at the top of the page)

        await ctx.send(f"{temperature}°C")

    # search anything and get the result featured by google (WIP)
    @commands.command()
    async def search(self, ctx, *, search):
        search.replace(" ", "+")

        search_url = requests.get(f"https://www.google.com/search?q={search}")
        search_soup = BeautifulSoup(search_url.text, "html.parser")

        search_results = search_soup.find("div", class_='Z0LcW', ).text
        await ctx.send(f"{search_results}")


def setup(client): # connect the cog to the bot
    client.add_cog(Search(client))



