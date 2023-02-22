# pip install sqlalchemy
# pip install chromedriver_autoinstaller
# pip install psycopg2
import os
import traceback
import re
from urllib.parse import quote
import sqlalchemy as db
from sqlalchemy.engine import create_engine
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller as AutoChrome
from logging.config import dictConfig
import logging
import datetime
import sys
from selenium.webdriver.common.keys import Keys
filePath, fileName = os.path.split(__file__)
logFolder = os.path.join(filePath , 'logs')
os.makedirs(logFolder, exist_ok = True)
logfilepath = os.path.join(logFolder, fileName.split('.')[0] + '_' + re.sub('-', '', str(datetime.date.today())) + '.log')
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s --- %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': logfilepath,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})         
# 로그 메시지 출력
def log(msg):
    logging.info(msg)
# 웹 알람 승인
def alarm_accept(driver):
    try:
        da = Alert(driver)
        da.accept()
    except:
        pass
# XPATH 이용 클릭(클릭이 가능할 때까지 암묵적 대기 3초)
def click_by_xpath(driver, xpath):
    try:
        target = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        target.click()
        return target
    except:
        log(f'######## ERROR : CLICK_BY_XPATH : {xpath}')
        log(traceback.format_exc())
        raise
# XPATH 이용 클릭(엘리먼트가 보일 때 까지)
def click_by_visible_xpath(driver, xpath):
    try:
        target =WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        target.click()
        return target
    except:
        log('######## ERROR : CLICK_BY_VISIBLE_XPATH')
        log(traceback.format_exc())
        raise
# 크롬드라이버 실행 및 옵션 설정 코드
def start_driver(driver_path, url, down_path = None):
    try:
        log('#### Start Driver')
        chrome_options = webdriver.ChromeOptions()
        # 서버 전용 옵션 활성화
        chrome_options.add_argument('--headless') # 보이지 않는 상태에서 작업
        chrome_options.add_argument('--window-size=1920x1080') # 보이지 않는 상태의 창 크기 설정
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--blink-setting=imagesEnable=false") ##페이지 로딩에서 이미지 제외
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument("--disable-gpu")
        # 다운로드 경로 변경 및 기타 옵션 설정
        if down_path == None:
            prefs = {
                'download.prompt_for_download': False,
                'download.directory_upgrade': True
                }
            chrome_options.add_experimental_option('prefs', prefs)
        else:
            prefs = {
                'download.default_directory': down_path,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
                }
            chrome_options.add_experimental_option('prefs', prefs)
        # 드라이브 시작
        driver = webdriver.Chrome(service = Service(driver_path), options = chrome_options)
        driver.implicitly_wait(100) # 대기 시작 설정
        driver.get(url) # URL 적용
        # 로딩 대기
        return driver
    except:
        log('######## ERROR :START DRIVER')
        log(traceback.format_exc())
        raise
