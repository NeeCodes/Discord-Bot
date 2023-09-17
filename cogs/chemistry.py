import discord, mendeleev
from discord.ext import commands

class Chemistry(commands.Cog): # inherits from commands.Cog

    def __init__(self, client):
        self.client = client

    # to create an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Chemistry initialised! :D")

    # search an element
    @commands.command(aliases = ['el'])
    async def element(self, ctx, search):
        search = search.capitalize()
        element = mendeleev.element(f'{search}')

        element_embed = discord.Embed(title = f"{element.name.capitalize()}", description =
        f'**Name:** {element.name} [{element.symbol}]'
        f'\n**Atomic Number:** {element.atomic_number}'
        f'\n**Atomic Weight:** {element.atomic_weight}'
        f'\n**electronic Configuration:** {element.econf}'
        f'\n**Oxidation States:** {element.oxistates}'
        f'\n**Position:** Group {element.group_id}, Period {element.period}, {element.block}-block'
        f'\n**Series:** {element.series}'

        f'\n\n**Description:** {element.description}'
        f'\n**Sources:** {element.sources}'
        f'\n**Uses:** {element.uses}'

        f'\n\n**Lattice Structure:** {element.lattice_structure}'
        f'\n**Atomic Radius:** {element.atomic_radius} pm'
        f'\n**Boiling Point:** {element.boiling_point} K'
        f'\n**Melementting Point:** {element.melting_point} K'
        f'\n**elementectron Affinity:** {element.electron_affinity} eV')

        await ctx.send(embed = element_embed)


def setup(client): # connect the cog to the bot
    client.add_cog(Chemistry(client))