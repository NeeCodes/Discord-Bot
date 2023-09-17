import discord, pytz, json
from discord.ext import commands
from datetime import datetime

class Time(commands.Cog): # inherits from commands.Cog

    def __init__(self, client):
        self.client = client

        try:
            with open("./data/saved_user_timezones.json", "r") as saved_user_timezones:
                self.user_timezone_dict = json.load(saved_user_timezones)

        except Exception:
            self.user_timezone_dict = {}

    # to create an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Time initialised! :D")

    # set timezone
    @commands.command(aliases = ['settz', 'settimezone'])
    async def set_timezone(self, ctx):
        global user_timezone_dict

        continents = ["", "Africa", "America", "Asia", "Atlantic", "Australia", "Canada", "Europe", "US"]

        msg_ask_continent = "Choose your region: \n\n"

        common_timezones = pytz.common_timezones

        for index, continent in enumerate(continents, start = 1):
            msg_choose_continent += f"{index}] {continent}\n"

        await ctx.send(f"{msg_choose_continent}")

        chosen_continent_index = await self.client.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 60)
        chosen_continent = continents[int(chosen_continent_index.content)]

        regions = []
        for timezone in common_timezones:
            if timezone.startswith(chosen_continent):
                regions.append(timezone)

        msg_choose_timezone = "Choose your timezone: \n \n"

        for i, timezone in enumerate(regions, start = 1):
            msg_choose_timezone += f"{i}] {timezone}  \n "
            if i % 50 == 0 and i > 0:
                await ctx.send(msg_choose_timezone)
                msg_choose_timezone = ""

        await ctx.send(f"{msg_choose_timezone}")

        chosen_timemzone = await self.client.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 60)
        user_timezone = regions[int(chosen_timemzone.content) - 1]
        user_timezone_dict[f"{ctx.author.id}"] = f"{user_timezone}"

        print(user_timezone_dict)
        await ctx.send(f"Success! Your timezone has been registered as: {user_timezone}")

        file = open("usertimezoneslist.json", "w")
        json.dump(user_timezone_dict, file)
        file.close()


    @commands.command(aliases = ['whattimeisit'])
    async def what_time_is_it(self, ctx, name):
        if name in user_timezone_dict.keys():
            user_timezone = pytz.timezone((user_timezone_dict[name]))
            current_time = datetime.now(pytz.common_timezones).strftime("%H:%M")
            await ctx.send(f"It is currently {current_time} for {name}")

        else:
            await ctx.send(f"Sorry, no timezone has been registered for {name}")

    @commands.command()
    async def timenow(self, ctx, user: discord.User):
        user_id = str(user.id)

        if user_id in user_timezone_dict:
            user_timezone = pytz.timezone(user_timezone_dict[user_id])
            current_time = datetime.now(user_timezone).strftime("%H:%M")
            await ctx.channel.send(f"It is currently {current_time} for {user.name}.")

        else:
            await ctx.channel.send(f"The user's timezone has not been registered.")


def setup(client): # connect the cog to the bot
    client.add_cog(Time(client))



