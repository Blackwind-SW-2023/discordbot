import lightbulb
import hikari
import random
import discord
from datetime import date
import sqlite3
import sys
import asyncio

sys.path.insert(0,'/home/dgist/discord/dgist_discord/background')
from background import update_hw

plugin = lightbulb.Plugin('projects')

def fetch_user_projects(username: str):
    # Connect to the database
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Execute a SELECT query to get all projects for the given username
    c.execute("SELECT project_name, deadline, course_name FROM projects WHERE username=?", (username,))
    projects = c.fetchall()
    
    # Close the connection
    conn.close()
    
    # Return the fetched projects
    return projects

def delete_project(project_name: str, course_name: str):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    try:
        c.execute("DELETE FROM projects WHERE project_name = ? AND course_name = ?", (project_name, course_name))
        conn.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

@plugin.command
@lightbulb.command('과제', '현존하는 과제 정보를 알려줍니다')
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def 과제(ctx: lightbulb.Context):
    username = "levicorpus"  # Replace with the actual username
    username = ctx.author.id
    projects = fetch_user_projects(username)
    
    # For debugging
    print(f"Projects for {username}:")
    for project_name, deadline, course_name in projects:
        await ctx.respond(f"```Project Name: {project_name}\n Deadline: {deadline}\n Course Name: {course_name}```")
    print("끝")

@과제.child
@lightbulb.command('업데이트', '과제 내용을 lms에서 가져옵니다', ephemeral=True)
@lightbulb.implements(lightbulb.PrefixSubGroup)
async def 업데이트(ctx: lightbulb.Context):
    await ctx.respond("업데이트중...")
    update_hw.update_hw(ctx.author.id)
    await ctx.respond("성공적으로 업데이트되었습니다.")

@과제.child
@lightbulb.command('등록', '과제 내용을 직접 추가합니다', ephemeral=True)
@lightbulb.implements(lightbulb.PrefixSubGroup)
async def 등록(ctx: lightbulb.Context):
    await ctx.respond("과제 내용을 직접 추가합니다")
    targetchannel = await ctx.bot.rest.create_dm_channel(ctx.author.id)
    await targetchannel.send("Please reply to this message with your project name.")
    
    def check(event: hikari.DMMessageCreateEvent):
        message = event.message
        is_valid = message.author.id == ctx.author.id
        return is_valid
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !과제 등록 command again.")
        return
    
    # Hash the password and store it in the database
    project_name = event.message.content.strip()
    # hashed_userid = bcrypt.hashpw(userid.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your deadline.")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !과제 등록 command again.")
        return
    
    # Hash the password and store it in the database
    deadline = event.message.content.strip()
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your course name.")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !과제 등록 command again.")
        return
    
    # Hash the password and store it in the database
    course_name = event.message.content.strip()
    # hashed_stud_num = bcrypt.hashpw(stud_num.encode('utf-8'), bcrypt.gensalt())
    
    # Saving data to the database
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    user_discord_id = ctx.author.id
    
    c.execute('''CREATE TABLE IF NOT EXISTS projects
             (project_id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL,
              project_name TEXT NOT NULL,
              deadline TEXT NOT NULL,
              course_name TEXT NOT NULL,
              UNIQUE(username, project_name, deadline, course_name))''')
    
    try:
        c.execute("INSERT INTO projects (username, project_name, deadline, course_name) VALUES (?, ?, ?, ?)", 
            (user_discord_id, project_name, deadline, course_name))
    except sqlite3.IntegrityError:
        print(f"Duplicate project detected and skipped.")
    
    conn.commit()
    conn.close()

    await targetchannel.send("과제 내용을 등록했습니다")

@과제.child
@lightbulb.command('삭제', '과제 내용을 삭제합니다')
@lightbulb.implements(lightbulb.PrefixSubGroup)
async def 삭제(ctx: lightbulb.Context):
    await ctx.respond("과제 내용을 직접 삭제합니다")
    targetchannel = await ctx.bot.rest.create_dm_channel(ctx.author.id)
    await targetchannel.send("Please reply to this message with your project name.")
    
    def check(event: hikari.DMMessageCreateEvent):
        message = event.message
        is_valid = message.author.id == ctx.author.id
        return is_valid
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !과제 삭제 command again.")
        return
    
    # Hash the password and store it in the database
    project_name = event.message.content.strip()
    # hashed_userid = bcrypt.hashpw(userid.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your course name.")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !과제 삭제 command again.")
        return
    
    # Hash the password and store it in the database
    course_name = event.message.content.strip()
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    delete_project(project_name, course_name)
    
    await targetchannel.send("과제 내용을 삭제했습니다")
    

def load(bot):
    bot.add_plugin(plugin)
