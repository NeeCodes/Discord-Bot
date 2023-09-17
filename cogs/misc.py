import discord, random
from discord.ext import commands
from datetime import date

class Misc(commands.Cog): # inherits from commands.Cog

    def __init__(self, client):
        self.client = client

    # to create an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Misc initialised! :D")

    # say hi
    @commands.command()
    async def hi(self, ctx):
        await ctx.send('hi')

    # you are (random percentage between 100 and 10000) cute
    @commands.command(aliases = ['howcuteis', 'howcute'])
    async def how_cute_is(self, ctx, *, name):
        percent = random.randint(100, 10000)

        await ctx.send(f"{name.capitalize()} is {percent}% cute.")

    # make the bot say something and delete the original message from the user calling the command
    @commands.command()
    async def say(self, ctx, *, say_this):
        await ctx.send(f"{say_this}")
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.client.process_commands(message)
        if message.author == self.client.user: # message from the bot itself
            return

        # reply to "I love you" with "I love you too!"
        if any(word in message.content.lower() for word in ["i love u", "i love you", "i lov u"]):
            await message.channel.send("I love you too!")

        # if a user says "I'm (x)", reply with "Hi (x) I'm dad"
        if message.content.startswith(("I'm", "i'm", "I'M")):
            user = message.content[4:] # the thing that the user says the are
            await message.channel.send(f"Hi {user} I'm Slavio")

        if message.content.startswith(("Im", "im", "IM")):
            user = message.content[3:]
            await message.channel.send(f"Hi {user} I'm Slavio")

        if message.content.startswith(("I am", "i am", "I AM")):
            user = message.content[5:]
            await message.channel.send(f"Hi {user} I'm Slavio")

        # reply to "hi", "hey", "hello" with "Hey :)"
        if message.content.lower().startswith(("hi", "hey", "hello")):
            await message.channel.send("Hey :)")

        # reply to "no u" with "no u"
        if 'no u' in message.content.lower():
            await message.channel.send("no u")

    # generate a fake quote from the mentioned user
    @commands.command(name = "quote", aliases = ['fakequote', 'fq'])
    async def quote(self, ctx, user: discord.User, *, quote):
        date = date.today().strftime("%d %B %Y") # date in the format d m y

        quote_embed = discord.Embed(description = f'> {quote}' f"\n  **    ** *- {user.name}, {date}*")
        quote_embed.set_author(name = f"{user.display_name}", icon_url = f"{user.avatar_url}")

        await ctx.send(embed = quote_embed)


def setup(client): # connect the cog to the bot
    client.add_cog(Misc(client))



