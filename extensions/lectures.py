import lightbulb
import hikari
import random
import datetime
from datetime import date
import sqlite3
import sys
import asyncio

sys.path.insert(0,'/home/dgist/discord/dgist_discord/background')
from background import update_timetable

plugin = lightbulb.Plugin('lectures')

def fetch_user_lectures(username: str):
    # Connect to the database
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Execute a SELECT query to get all projects for the given username
    c.execute("SELECT day_of_week, lecture_code, start_time, end_time, lecture_name, location, professor_name FROM lectures WHERE username=?", (username,))
    lectures = c.fetchall()
    
    print(lectures)
    
    # Close the connection
    conn.close()
    
    # Return the fetched projects
    return lectures

def delete_schedule(day_of_week: int, start_time: int):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    try:
        c.execute("DELETE FROM lectures WHERE day_of_week = ? AND start_time = ?", (day_of_week, start_time))
        conn.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

def calculate_number(time_str):
        # Parse the input time string to a datetime object
        input_time = datetime.datetime.strptime(time_str, '%H.%M')
        # Define the reference time "08:00"
        reference_time = datetime.datetime.strptime('08.00', '%H.%M')
        # Calculate the time difference
        time_difference = input_time - reference_time
        # If the time difference is negative, return 0 or handle accordingly
        if time_difference < datetime.timedelta():
            return 0
        # Calculate the quotient of the time difference divided by 30 minutes
        number = time_difference.total_seconds() // (30 * 60)  # 30 minutes in seconds
        return int(number)

def get_day_index(input_string):
    days_of_week = ["mon", "tues", "wed", "thu", "fri", "sat", "sun"]
    for i, day in enumerate(days_of_week):
        if day in input_string.lower():  # Convert input_string to lowercase and check if day is present in it
            return i
    return -1  # Return -1 if no day of the week is found in the input_string

def handleweekday(ctx: lightbulb.Context, weekdayidx: int):
    username = "levicorpus"  # Replace with the actual username
    username = ctx.author.id
    all_lectures = fetch_user_lectures(username)
    
    print(all_lectures)

    weekday_list = ["월", "화", "수", "목", "금"]
    whole_msg = f"* {weekday_list[weekdayidx]}요일 수업\n"
    
    nosooup = True

    find_starttime = lambda lecture: lecture[2]
    
    for lecture in sorted(all_lectures, key=find_starttime):
        weekday_lec, code, start, end, name, room, prof = lecture
        if weekday_lec != weekdayidx:
            continue
        nosooup = False
        starttime = f"{start // 2 + 8}:{(start % 2)*30:02}"
        endtime = f"{end // 2 + 8}:{(end % 2)*30:02}"

        whole_msg += f"```과목 이름: {name}\n 과목 코드: {code}\n 시작 시간: {starttime}\n 끝 시간: {endtime}\n 강의실: {room}\n 교수: {prof}```"

    if nosooup:
        whole_msg = "이 날은 수업이 없습니다!"
    return whole_msg

def default(ctx: lightbulb.Context):
    username = "levicorpus"  # Replace with the actual username
    username = ctx.author.id
    all_lectures = fetch_user_lectures(username)

    now = datetime.datetime.now()
    print(now)
    time_now = now.time()
    print(time_now)
    
    if now.date().weekday() > 4:   # 토, 일
        return "오늘은 수업이 없습니다!"

    weekday_list = ["월", "화", "수", "목", "금"]
    whole_msg = f"* {weekday_list[now.date().weekday()]}요일 남은 수업\n"

    find_starttime = lambda lecture: lecture[2]
    
    for lecture in sorted(all_lectures, key=find_starttime):
        weekday_lec, code, start, end, name, room, prof = lecture
        if weekday_lec != now.date().weekday():    continue

        starttime = f"{start // 2 + 8}:{(start % 2)*30:02}"
        endtime = f"{end // 2 + 8}:{(end % 2)*30:02}"

        if starttime < time_now:        continue
        whole_msg += f"```과목 이름: {name}\n 과목 코드: {code}\n 시작 시간: {starttime}\n 끝 시간: {endtime}\n 강의실: {room}\n 교수: {prof}```"

    return whole_msg

def 전체(ctx: lightbulb.Context):
    username = "levicorpus"  # Replace with the actual username
    username = ctx.author.id
    all_lectures = fetch_user_lectures(username)
    
    now = datetime.datetime.now()
    time_now = now.time()

    whole_msg = ""
    weekday_list = ["월", "화", "수", "목", "금"]
    
    find_starttime = lambda lecture: lecture[2]

    for weekday in range(len(weekday_list)):
        whole_msg += f"* {weekday_list[weekday]}요일 수업\n"

        for lecture in sorted(all_lectures, key=find_starttime):
            weekday_lec, code, start, end, name, room, prof = lecture
            
            if weekday_lec != weekday:
                print("a")
                continue

            starttime = f"{start // 2 + 8}:{(start % 2)*30:02}"
            endtime = f"{end // 2 + 8}:{(end % 2)*30:02}"
            
            whole_msg += f"```과목 이름: {name}\n 과목 코드: {code}\n 시작 시간: {starttime}\n 끝 시간: {endtime}\n 강의실: {room}\n 교수: {prof}```"

    return whole_msg

@plugin.command
@lightbulb.option('weekday', '요일 정보', required=False, type=str)
@lightbulb.command('수업', '현재 시간 이후로 남은 오늘 수업 정보를 알려줍니다.')
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def 수업(ctx: lightbulb.Context):
    weekday_list = ["월", "화", "수", "목", "금"]
    if ctx.options.weekday == None:             # !수업
        await ctx.respond(default(ctx))
        return
    if ctx.options.weekday == "전체":           # !수업 전체
        await ctx.respond(전체(ctx))
        return
    for i, weekday in enumerate(weekday_list):
        if ctx.options.weekday == weekday:      # !수업 [요일]
            await ctx.respond(handleweekday(ctx, i))
            return

@수업.child
@lightbulb.command('업데이트', '수업 정보를 업데이트합니다')
@lightbulb.implements(lightbulb.PrefixSubGroup)
async def 업데이트(ctx: lightbulb.Context):
    await ctx.respond("업데이트중...")
    update_timetable.update_timetable(ctx.author.id)
    await ctx.respond("성공적으로 업데이트되었습니다.")

@수업.child
@lightbulb.command('등록', '일정을 직접 추가합니다')
@lightbulb.implements(lightbulb.PrefixSubGroup)
async def 등록(ctx: lightbulb.Context):
    await ctx.respond("일정을 직접 추가합니다")
    targetchannel = await ctx.bot.rest.create_dm_channel(ctx.author.id)
    await targetchannel.send("Please reply to this message with the day of the week of the schedule (in short). e.g. mon")
    
    def check(event: hikari.DMMessageCreateEvent):
        message = event.message
        is_valid = message.author.id == ctx.author.id
        return is_valid
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !수업 등록 command again.")
        return
    
    # Hash the password and store it in the database
    day_of_week = get_day_index(event.message.content.strip())
    # hashed_userid = bcrypt.hashpw(userid.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your start time and end time (in [hour].[minute] format), seperated with space. e.g. 10.30 12.00")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the /등록 command again.")
        return
    
    # Hash the password and store it in the database
    start_time, end_time  = [calculate_number(str_num.strip(' ')) for str_num in event.message.content.strip().split(' ')]
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your schedule name.")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !수업 등록 command again.")
        return
    
    # Hash the password and store it in the database
    lecture_name = event.message.content.strip()
    # hashed_stud_num = bcrypt.hashpw(stud_num.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your schedule location.")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !수업 등록 command again.")
        return
    
    # Hash the password and store it in the database
    location = event.message.content.strip()
    # hashed_stud_num = bcrypt.hashpw(stud_num.encode('utf-8'), bcrypt.gensalt())
    
    # Saving data to the database
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    user_discord_id = ctx.author.id
    
    # create lectures table
    c.execute('''CREATE TABLE IF NOT EXISTS lectures
             (lecture_id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL,
              day_of_week INTEGER NOT NULL,
              lecture_code TEXT NOT NULL,
              start_time INTEGER NOT NULL,
              end_time INTEGER NOT NULL,
              lecture_name TEXT NOT NULL,
              location TEXT NOT NULL,
              professor_name TEXT NOT NULL,
              UNIQUE(username, day_of_week, lecture_code, start_time, end_time, lecture_name, location, professor_name))''')
    
    try:
        c.execute('''INSERT INTO lectures 
                    (username, day_of_week,  lecture_code, start_time, end_time, lecture_name, location, professor_name) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (user_discord_id, day_of_week, "None", start_time, end_time, lecture_name, location, "None"))
    except sqlite3.IntegrityError:
        print(f"Duplicate lecture detected and skipped")
    
    conn.commit()
    conn.close()

    await targetchannel.send("일정을 등록했습니다")

@수업.child
@lightbulb.command('삭제', '교직원 학식 정보를 불러옵니다')
@lightbulb.implements(lightbulb.PrefixSubGroup)
async def 삭제(ctx: lightbulb.Context):
    await ctx.respond("일정을 직접 삭제합니다")
    targetchannel = await ctx.bot.rest.create_dm_channel(ctx.author.id)
    await targetchannel.send("Please reply to this message with the day of the week of the schedule (in short). e.g. mon")
    
    def check(event: hikari.DMMessageCreateEvent):
        message = event.message
        is_valid = message.author.id == ctx.author.id
        return is_valid
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !수업 삭제 command again.")
        return
    
    # Hash the password and store it in the database
    day_of_week = get_day_index(event.message.content.strip())
    # hashed_userid = bcrypt.hashpw(userid.encode('utf-8'), bcrypt.gensalt())
    
    await targetchannel.send("Please reply to this message with your starting time of the schedule e.g. 10.00")
    
    try:
        event = await ctx.bot.wait_for(hikari.DMMessageCreateEvent, timeout=60, predicate=check)
    except asyncio.TimeoutError:
        await targetchannel.send("Registration timed out, please try the !수업 삭제 command again.")
        return
    
    # Hash the password and store it in the database
    start_time = calculate_number(event.message.content.strip())
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    delete_schedule(day_of_week, start_time)
    
    await targetchannel.send("일정 내용을 삭제했습니다")

def load(bot):
    bot.add_plugin(plugin)
