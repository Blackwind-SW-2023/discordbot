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
from naver_login import get_auth_pop3

# from background import _DRIVER_PATH

# DRIVER_PATH = _DRIVER_PATH

# service = Service(executable_path=DRIVER_PATH)
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
# options.add_argument("--window-size=1024x768")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

def update_food_json():
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
            id_tab.send_keys("levicorpus")
            pw_tab = driver.find_element(By.ID, "password")
            pw_tab.send_keys("vdwA79877#")
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
        auth_num = get_auth_pop3("dgistlogin", "komaruN12#$")

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
        driver.get("https://my.dgist.ac.kr/com/portal/index.do?goPage=")
        time.sleep(1)
        if driver.title == 'DGIST Portal': break
    
    print("adsfasdf")
    
    # 연구동
    driver.find_element(By.XPATH, '//*[@id="CMN99.02"]').click()
    driver.implicitly_wait(3)
    ygd_dinner = ygd_lunch = ''
    try:
        while ygd_lunch == '':
            driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/div[1]/div/a[2]').click()
            time.sleep(3)
            if '중식' in driver.find_element(By.XPATH, '//*[@id="tab2_1"]/ul/li[1]/h4').text:
                ygd_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_1"]/ul/li[1]/div').text
                if ygd_lunch == '': ygd_lunch = "오늘은 식단정보가 등록되지 않았습니다"
            elif '중식' in driver.find_element(By.XPATH, '//*[@id="tab2_1"]/ul/li[2]/h4').text:
                ygd_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_1"]/ul/li[2]/div').text
                if ygd_lunch == '': ygd_lunch = "오늘은 식단정보가 등록되지 않았습니다"
    except NoSuchElementException: ygd_lunch = "오늘은 식단정보가 등록되지 않았습니다"
    try:
        while ygd_dinner == '':
            driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/div[1]/div/a[2]').click()
            time.sleep(3)
            if '석식' in driver.find_element(By.XPATH, '//*[@id="tab2_1"]/ul/li[1]/h4').text:
                ygd_dinner = driver.find_element(By.XPATH, '//*[@id="tab2_1"]/ul/li[1]/div').text
                if ygd_dinner == '': ygd_dinner = "오늘은 식단정보가 등록되지 않았습니다"
            elif '석식' in driver.find_element(By.XPATH, '//*[@id="tab2_1"]/ul/li[2]/h4').text:
                ygd_dinner = driver.find_element(By.XPATH, '//*[@id="tab2_1"]/ul/li[2]/div').text
                if ygd_dinner == '': ygd_dinner = "오늘은 식단정보가 등록되지 않았습니다"
    except NoSuchElementException: ygd_dinner = "오늘은 식단정보가 등록되지 않았습니다"
    
    # 학생식당
    driver.find_element(By.XPATH, '//*[@id="CMN99.01"]').click()
    driver.implicitly_wait(3)
    hk_nm_lunch = hk_sp_lunch = hk_dinner = ''
    try:
        while hk_nm_lunch == '':
            driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/div[1]/div/a[2]').click()
            time.sleep(3)
            if '일반식' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[1]/h4').text:
                hk_nm_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[1]/div').text
                if hk_nm_lunch == '': hk_nm_lunch = "오늘은 식단정보가 등록되지 않았습니다"
            elif '일반식' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[2]/h4').text:
                hk_nm_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[2]/div').text
                if hk_nm_lunch == '': hk_nm_lunch = "오늘은 식단정보가 등록되지 않았습니다"
            elif '일반식' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[3]/h4').text:
                hk_nm_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[3]/div').text
                if hk_nm_lunch == '': hk_nm_lunch = "오늘은 식단정보가 등록되지 않았습니다"
            elif '일반식' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[4]/h4').text:
                hk_nm_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[4]/div').text
                if hk_nm_lunch == '': hk_nm_lunch = "오늘은 식단정보가 등록되지 않았습니다"
    except NoSuchElementException: hk_nm_lunch = "오늘은 식단정보가 등록되지 않았습니다"
    try:
        while hk_sp_lunch == '':
            driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/div[1]/div/a[2]').click()
            time.sleep(3)
            if '일품' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[1]/h4').text:
                hk_sp_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[1]/div').text
                if hk_sp_lunch == '': hk_sp_lunch = "오늘은 식단정보가 등록되지 않았습니다"
            elif '일품' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[2]/h4').text:
                hk_sp_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[2]/div').text
                if hk_sp_lunch == '': hk_sp_lunch = "오늘은 식단정보가 등록되지 않았습니다"
            elif '일품' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[3]/h4').text:
                hk_sp_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[3]/div').text
                if hk_sp_lunch == '': hk_sp_lunch = "오늘은 식단정보가 등록되지 않았습니다"
            elif '일품' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[4]/h4').text:
                hk_sp_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[4]/div').text
                if hk_sp_lunch == '': hk_sp_lunch = "오늘은 식단정보가 등록되지 않았습니다"
    except NoSuchElementException: hk_sp_lunch = "오늘은 식단정보가 등록되지 않았습니다"
    try:
        while hk_dinner == '':
            driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/div[1]/div/a[2]').click()
            time.sleep(3)
            if 'A코너' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[1]/h4').text:
                hk_dinner = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[1]/div').text
                if hk_dinner == '': hk_dinner = "오늘은 식단정보가 등록되지 않았습니다"
            elif 'A코너' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[2]/h4').text:
                hk_dinner = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[2]/div').text
                if hk_dinner == '': hk_dinner = "오늘은 식단정보가 등록되지 않았습니다"
            elif 'A코너' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[3]/h4').text:
                hk_dinner = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[3]/div').text
                if hk_dinner == '': hk_dinner = "오늘은 식단정보가 등록되지 않았습니다"
            elif 'A코너' in driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[4]/h4').text:
                hk_dinner = driver.find_element(By.XPATH, '//*[@id="tab2_2"]/ul/li[4]/div').text
                if hk_dinner == '': hk_dinner = "오늘은 식단정보가 등록되지 않았습니다"
    except NoSuchElementException: hk_dinner = "오늘은 식단정보가 등록되지 않았습니다"
    
    # 교직원
    driver.find_element(By.XPATH, '//*[@id="CMN99.03"]').click()
    driver.implicitly_wait(3)
    gjw_lunch = ''
    try:
        gjw_lunch = driver.find_element(By.XPATH, '//*[@id="tab2_3"]/ul/li/div').text
        if gjw_lunch == '': gjw_lunch = "오늘은 식단정보가 등록되지 않았습니다"
        time.sleep(3)
    except NoSuchElementException:
        gjw_lunch = "오늘은 식단정보가 등록되지 않았습니다"

    driver.quit()

    food_info = {
        "ygd_lunch" : ygd_lunch,
        "ygd_dinner" : ygd_dinner,
        "hk_nm_lunch" : hk_nm_lunch,
        "hk_sp_lunch" : hk_sp_lunch, 
        "hk_dinner" : hk_dinner,
        "gjw_lunch" : gjw_lunch
    }

    # print(*food_info.values(), sep='\n')

    with open("food.json", "w") as outfile:
        json.dump(food_info, outfile)

update_food_json()
print("updated")