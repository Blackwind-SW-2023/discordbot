import lightbulb
import hikari
import random
from datetime import date

plugin = lightbulb.Plugin('Example')

def roll_dice(probability:float)->bool:
    num = random.randint(0,100)
    if num <= probability:
        return True
    return False

# @plugin.listener(hikari.GuildMessageCreateEvent)
# async def on_message_event(event):
#     # if roll_dice(5):
#     #     await event.message.respond("응 개강해")
#     print(event.content)

# @plugin.listener(hikari.GuildMessageDeleteEvent)
# async def on_message_delete(event):
#     await event.message.respond("이걸 지우네")

@plugin.command
@lightbulb.command('ping', 'says pong')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("Pong")

def load(bot):
    bot.add_plugin(plugin)
    
print(date.today())