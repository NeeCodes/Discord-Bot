import discord, random
from discord.ext import commands

class WYR(commands.Cog): # inherits from commands.Cog

    def __init__(self, client):
        self.client = client

        with open("assets/wyr_questions.txt", "r", encoding = "utf-8") as questions_file:
            self.wyr_questions = []

            for question in questions_file.readlines():
                question = question.rstrip("\n")
                question = question.split(" ")
                question.pop(0)

                question = " ".join(question)
                
                self.wyr_questions.append(question)

    # to create an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("WYR initialised! :D")

    # would you rather command, sends a random would you rather question from a set of them
    @commands.command()
    async def wyr(self, ctx):
        wyr_embed = discord.Embed(description = f"{random.choice(self.wyr_questions)}", colour = COLOUR)
        await ctx.send(embed = wyr_embed)


def setup(client): # connect the cog to the bot
    client.add_cog(WYR(client))



