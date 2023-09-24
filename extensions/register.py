import lightbulb
import hikari
import asyncio
from datetime import date
import sqlite3

plugin = lightbulb.Plugin('register')

def get_user_id(username: str):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute("SELECT id FROM id WHERE username=?", (username,))
    user = c.fetchone()
    
    conn.close()
    
    return user[0] if user else None

def get_password(username: str):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute("SELECT password FROM password WHERE username=?", (username,))
    user = c.fetchone()
    
    conn.close()
    
    return user[0] if user else None

@plugin.command
@lightbulb.command('등록', '아이디 비번을 등록합니다. 이는 사용자 수업 정보를 가져오기 위해 사용됩니다.', ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def register(ctx: lightbulb.Context):
    await ctx.respond("User registration process")
    targetchannel = await ctx.bot.rest.create_dm_channel(ctx.author.id)
    await targetchannel.send("Please reply to this message with your ID.")
    
    def check(event: hikari.DMMessageCreateEvent):
        message = event.message
        is_valid = message.author.id == ctx.author.id
        return is_valid
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the /등록 command again.")
        return
    
    # Hash the password and store it in the database
    userid = event.message.content.strip()
    # hashed_userid = bcrypt.hashpw(userid.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your password.")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the /등록 command again.")
        return
    
    # Hash the password and store it in the database
    password = event.message.content.strip()
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your student number.")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the /등록 command again.")
        return
    
    # Hash the password and store it in the database
    stud_num = event.message.content.strip()
    # hashed_stud_num = bcrypt.hashpw(stud_num.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your naver id.")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the /등록 command again.")
        return
    
    # Hash the password and store it in the database
    naver_id = event.message.content.strip()
    # hashed_stud_num = bcrypt.hashpw(stud_num.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your naver password.")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the /등록 command again.")
        return
    
    # Hash the password and store it in the database
    naver_pw = event.message.content.strip()
    # hashed_stud_num = bcrypt.hashpw(stud_num.encode('utf-8'), bcrypt.gensalt())
    
    # Saving data to the database
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    user_discord_id = ctx.author.id
    
    # Insert a new user or replace the existing user if user_id already exists
    c.execute("INSERT OR REPLACE INTO id (username, id) VALUES (?, ?)", (user_discord_id, userid))
    # Insert a new user or replace the existing user if user_id already exists
    c.execute("INSERT OR REPLACE INTO password (username, password) VALUES (?, ?)", (user_discord_id, password))
    # Insert a new user or replace the existing user if user_id already exists
    c.execute("INSERT OR REPLACE INTO studnumber (username, studnumber) VALUES (?, ?)", (user_discord_id, stud_num))
    # Insert a new user or replace the existing user if user_id already exists
    c.execute("INSERT OR REPLACE INTO naver_id (username, naver_id) VALUES (?, ?)", (user_discord_id, naver_id))
    # Insert a new user or replace the existing user if user_id already exists
    c.execute("INSERT OR REPLACE INTO naver_pw (username, naver_pw) VALUES (?, ?)", (user_discord_id, naver_pw))
    
    conn.commit()
    conn.close()

    await targetchannel.send("사용자 정보를 등록했습니다")

@plugin.command
@lightbulb.command('내정보', '등록된 자신의 정보를 표시합니다. 본인만 볼 수 있습니다', ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def myinfo(ctx: lightbulb.Context):
    user = ctx.author
    user_id = user.id
    
    registered_id = get_user_id(user_id)
    registered_pw = get_password(user_id)
    
    embed = hikari.Embed(
        title=f"{user.username}",
        description=f"registered id: {registered_id}\nregistered pw: {registered_pw}",
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
    
