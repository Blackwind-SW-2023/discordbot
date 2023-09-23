import lightbulb
import hikari
import random
import discord
from datetime import date
import bcrypt
import sqlite3

def register_user(user_id: int, password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO users (user_id, hashed_password) VALUES (?, ?)", (user_id, hashed_password))
    
    conn.commit()
    conn.close()

plugin = lightbulb.Plugin('register')

@plugin.command
@lightbulb.option('pw', "사용자의 비번")
@lightbulb.option('id', "사용자의 아이디")
@lightbulb.command('등록', '아이디 비번을 등록합니다. 이는 사용자 수업 정보를 가져오기 위해 사용됩니다.', ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def register(ctx: lightbulb.Context):
    await ctx.respond("사용자 정보를 등록했습니다")

@plugin.command
@lightbulb.command('내정보', '등록된 자신의 정보를 표시합니다. 본인만 볼 수 있습니다', ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def myinfo(ctx: lightbulb.Context):
    user = ctx.author
    
    embed = hikari.Embed(
        title=f"{user.username}#{user.discriminator}",
        description=f"user id: {user.id}",
        color=hikari.Color(0x1ABC9C),  # You can choose a color that suits your preference
    )
    
    embed.set_thumbnail(user.avatar_url)
    embed.add_field(name="Joined Discord on", value=user.created_at.strftime("%B %d, %Y"))
    if user.is_bot:
        embed.add_field(name="Bot", value="Yes")
    else:
        embed.add_field(name="Bot", value="No")
    
    await ctx.respond(embed=embed)

def load(bot):
    bot.add_plugin(plugin)
    
