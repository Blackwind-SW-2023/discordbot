from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import sqlite3
import sys

def crawl_hw(userid, userpw):
    # DRIVER_PATH = "/drivers/geckodriver"
    # service = Service(executable_path=DRIVER_PATH)

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    while True:
        try:
            driver = webdriver.Firefox(options=options)
            break
        except WebDriverException as e:
            sys.stderr.write(f'Exception in Loading FireFox: {e.msg}\n')
            continue

    while True:
        try:
            # Open the login page
            driver.get("https://dgist.blackboard.com/")
            break
        except NoSuchElementException or TimeoutException:
            continue

    driver.implicitly_wait(3)
    
    print("here")

    while True:
        try:
            # Open the login page
            driver.find_element(By.XPATH, '//*[@id="agree_button"]').click()
            break
        except NoSuchElementException or TimeoutException:
            continue
    print("here")

    while True:
        try:
            # Open the login page
            username_elem = driver.find_element(By.XPATH, '//*[@id="portal_username"]')
            password_elem = driver.find_element(By.XPATH, '//*[@id="portal_password"]')
            login_button = driver.find_element(By.XPATH, '//*[@id="portal"]')

            # Type the username and password
            username_elem.send_keys(userid)
            password_elem.send_keys(userpw)

            # Click the login button
            login_button.click()
            break
        except NoSuchElementException or TimeoutException or TypeError:
            continue

    # driver.implicitly_wait(time_to_wait=15)
    print("here")

    while True:
        try:
            # 활동 스크림으로 이동
            driver.get("https://lms.dgist.ac.kr/ultra/calendar")
            break
        except NoSuchElementException or TimeoutException:
            continue

    driver.implicitly_wait(3)

    print("here")
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@id="bb-calendar1-month"]').click()
            driver.implicitly_wait(time_to_wait=1)
            driver.find_element(By.XPATH, '//*[@id="bb-calendar1-deadline"]').click()
            driver.implicitly_wait(time_to_wait=1)
            break
        except NoSuchElementException or TimeoutException:
            continue

    project_names = []
    deadlines = []
    course_names = []

    print("here")
    while True:
        try:
            # 각 요소의 텍스트 가져와 리스트에 추가하기
            for project_name_element in driver.find_elements(By.CSS_SELECTOR, "div.name > a"):
                project_names.append(project_name_element.text)

            for deadline_element in driver.find_elements(By.CSS_SELECTOR, "div.content > span"):
                deadline = deadline_element.text.replace("마감일: ", "")
                if deadline != ".": deadlines.append(deadline)

            for course_name_element in driver.find_elements(By.CSS_SELECTOR, "div.content > a"):
                course_names.append(course_name_element.text)
            break
        except NoSuchElementException or TimeoutException:
            continue

    driver.quit()

    return project_names, deadlines, course_names

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

def update_hw(username):
    # Define your SQLite Connection and Cursor here
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    userid = get_user_id(username)
    print(userid)
    userpw = get_password(username)
    print(userpw)

    # Your retrieved data
    project_names, deadlines, course_names = crawl_hw(userid, userpw)
    
    # print("yessss")
    
    c.execute('''CREATE TABLE IF NOT EXISTS projects
             (project_id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL,
              project_name TEXT NOT NULL,
              deadline TEXT NOT NULL,
              course_name TEXT NOT NULL,
              UNIQUE(username, project_name, deadline, course_name))''')

    # Inserting data into the database
    for project_name, deadline, course_name in zip(project_names, deadlines, course_names):
        try:
            c.execute("INSERT INTO projects (username, project_name, deadline, course_name) VALUES (?, ?, ?, ?)", 
                (username, project_name, deadline, course_name))
        except sqlite3.IntegrityError:
            print(f"Duplicate project detected and skipped.")

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
