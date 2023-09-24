import requests
import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import MaxRetryError
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time
import json
import random
import sqlite3
from naver_login import get_auth_pop3

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

def loginAndGetLecture(studnumber, userid, userpw, naver_id, naver_pw):
    while True:
        try:
            driver = webdriver.Firefox(options=options)
        except WebDriverException:
            continue
        break
    while True:
        try: driver.get("https://auth.dgist.ac.kr/login/?agentId=22")
        except MaxRetryError:
            time.sleep(random.randint(2,5))
            continue
        try:
            id_tab = driver.find_element(By.ID, "loginID")
            id_tab.send_keys(userid)
            pw_tab = driver.find_element(By.ID, "password")
            pw_tab.send_keys(userpw)
            pw_tab.send_keys(Keys.ENTER)

            driver.implicitly_wait(2)

            pw_expired = False
            if WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'alert_btn'))):
                alert = driver.find_element(By.ID, "alert_btn") #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'alert_btn')))
                alert.click()
                pw_expired = True

            if pw_expired:
                driver.implicitly_wait(2)
                change_later = driver.find_element(By.CSS_SELECTOR, "body > div.body > div.container > div.button-area.submit > button.button.bg-g")
                change_later.click()
                driver.implicitly_wait(2)

            parent = driver.current_window_handle
            uselessWindows = driver.window_handles
            for winId in uselessWindows:
                if winId != parent: 
                    driver.switch_to.window(winId)
                    driver.close()
            driver.switch_to.window(parent)

            time.sleep(2)

            if WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'alert_btn'))):
                alert = driver.find_element(By.ID, "alert_btn") #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'alert_btn')))
                alert.click()
        except: continue
        time.sleep(3)
        auth_num = get_auth_pop3(naver_id, naver_pw)

        driver.find_element(By.ID, 'code').send_keys(auth_num)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/button').click()

        driver.implicitly_wait(2)
        try:
            alert = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "alert_btn")))
            alert_msg = driver.find_element(By.XPATH, '//*[@id="alert_body"]').text
            if alert_msg == "로그인 실패하였습니다. 다시 시도해주세요.":
                continue
            alert = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "alert_btn")))
            alert.click()
            driver.implicitly_wait(2)
        except TimeoutException: continue
        driver.get("https://stud.dgist.ac.kr")
        time.sleep(1)
        if driver.title == '학생정보광장': break
    
    cookie=driver.get_cookie("JSESSIONID")
    
    print(cookie)
    
    return getLectures(studnumber, cookie['value'])
    

#firefox ver
def getLectures(studnumber,cookie):
    # studnumber='202011120'
    #need sessionid
    # jsessionid=driver.get_cookie("JSESSIONID")
    # cookie='Zjf1ygZx86HZlmO2CWPzYAlXPzX1lMzSHsX4iaAL2nTIrf2KnputEXcGFQqRwNym.aGFrc2FfZG9tYWluL2hha3NhMV9zdHVkMQ=='
    cookies = {
        'JSESSIONID': cookie}

    headers = {
        'Connection': 'keep-alive',
        'Origin': 'https://stud.dgist.ac.kr',
        'Referer': 'https://stud.dgist.ac.kr/ucr/ucrqStudtTmTbl/index.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ko,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'sec-ch-ua': '"Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'pageNum': '1',
        'pageSize': '9999',
        'sortName': '',
        'sortOrder': '',
        'commonMenuId': '',
        'commonProgramId': 'UcrqStudtTmTbl',
        'sttsMenuYn': '',
        'dummytext': '',
        'searchShyyShtm': '2023/CMN17.20',
        'searchYear': '',
        'searchTerm': '',
        'searchOrgn': 'CMN12.03',
        'searchStdNo': studnumber,
        'searchSpclLec': 'N',
        'searchLang': 'KOR',
        '_search': 'false',
        'rows': '9999',
        'page': '1',
        'sidx': '',
        'sord': 'asc',
    }

    response = requests.post('https://stud.dgist.ac.kr/ucr/ucrqStudtTmTbl/list.do', cookies=cookies, headers=headers, data=data)

    my_json = response.content.decode('utf8').replace("'", '"')
    # print(my_json)
    json_data = json.loads(my_json)
    d=json_data['user']
    days=[['']*35 for i in range(5)]
    daysdata=[['']*35 for i in range(5)]
    for i, data in enumerate(d):
        for idx,day in enumerate(["MON","THU","WED","TUR","FRI"]):
            if day in data:
                t=data[day].split('\n')
                days[idx][i]=(t[0])
                daysdata[idx][i]=(t[1:])
    final=[list() for i in range(5)]
    for day in range(5):
        subjects=days[day]
        prename=''
        prestart=''
        for i,subject in enumerate(subjects):
            if subject==prename:
                continue
            if prename=='':
                prename=subject
                prestart=i
                continue
            #다를 때
            final[day].append((prename,prestart,i-1,*daysdata[day][i-1]))
            prename=subject
            prestart=i
    return final

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

def get_stud_num(username: str):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute("SELECT studnumber FROM studnumber WHERE username=?", (username,))
    user = c.fetchone()
    
    conn.close()
    
    return user[0] if user else None

def get_naver_id(username: str):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute("SELECT naver_id FROM naver_id WHERE username=?", (username,))
    user = c.fetchone()
    
    conn.close()
    
    return user[0] if user else None

def get_naver_pw(username: str):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute("SELECT naver_pw FROM naver_pw WHERE username=?", (username,))
    user = c.fetchone()
    
    conn.close()
    
    return user[0] if user else None

def update_timetable(username):
    # Define your SQLite Connection and Cursor here
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    userid = get_user_id(username)
    print(userid)
    userpw = get_password(username)
    print(userpw)
    studnumber = get_stud_num(username)
    print(studnumber)
    naver_id = get_naver_id(username)
    print(naver_id)
    naver_pw = get_naver_pw(username)
    print(naver_pw)
    
    # Received data
    lectureInfo = loginAndGetLecture(studnumber, userid, userpw, naver_id, naver_pw)
    
    def reorganize_data(student_id, original_data):
        days_of_week = list(range(5))
        reformatted_data = []
        for day, lectures in zip(days_of_week, original_data):
            reformatted_lectures = [(student_id, day, *lecture) for lecture in lectures]
            reformatted_data.append(reformatted_lectures)
        return reformatted_data
    
    # Create the lectures table
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
    
    # Reorganize data so that it matches db format
    organized = reorganize_data(username,lectureInfo)
    
    try:
        for lectures in organized:
            for lecture in lectures:
                try:
                    c.execute('''INSERT INTO lectures 
                                (username, day_of_week,  lecture_code, start_time, end_time, lecture_name, location, professor_name) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', lecture)
                except sqlite3.IntegrityError:
                    print(f"Duplicate lecture detected and skipped: {lecture}")
        conn.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()