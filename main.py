import discord
import os
from discord.ext import commands, tasks
from itertools import cycle

TOKEN = ('insert-your-token-here')

client = commands.Bot(command_prefix = '!')

status = cycle(["never gonna give you up", "never gonna let you down"])

owners = [] 

def is_owner(ctx):
    if ctx.message.author.id in owners:
        return True
    return False

# remove the default help command so that it can be replaced by the custom help command
client.remove_command('help')

# load cog into the main bot
@client.command()
async def load(ctx, extension):
    if is_owner(ctx):
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been loaded successfully.")

    else:
        await ctx.send("You are not authorised to perform this action.")

# unload cog
@client.command()
async def unload(ctx, extension):
    if is_owner(ctx):
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been unloaded successfully.")

    else:
        await ctx.send("You are not authorised to perform this action.")

# reload cog
@client.command()
async def reload(ctx, extension):
    if is_owner(ctx):
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been reloaded successfully.")

    else:
        await ctx.send("You are not authorised to perform this action.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != 'constants.py':
        client.load_extension(f'cogs.{filename[:-3]}') # [:-3] is to remove the .py from the filename


client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    change_status.start()
    print("hello world")

@tasks.loop(seconds = 5)
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))

client.run(TOKEN)