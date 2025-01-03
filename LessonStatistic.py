import pytest
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('URL')
username= os.getenv('USERNAME_TEACHER')
password = os.getenv('PASSWORD_TEACHER')
text_discipline = os.getenv('TEXT_DISCIPLINE')
topic_text = f'Введение в {text_discipline}'

@pytest.fixture
def test_true_login(setup_browser):
    driver = setup_browser

    driver.get(url)

    login_field = driver.find_element('id', 'username')
    login_field.send_keys(username)

    password_field = driver.find_element('id', 'password')
    password_field.send_keys(password)

    login_button = driver.find_element('xpath', "//button[text()='Войти']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  
    login_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('xpath', "//h1[@class='teacher-lessons__main-container-title']"))
    )

    assert driver.current_url == url + 'teacher-lessons'
    return driver

# Статистика пары
def test_lesson_statistic(test_true_login):
    driver = test_true_login

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(('class name', 'teacher-lessons__search-input'))
    )

    input_field = driver.find_element('class name', 'teacher-lessons__search-input')
    input_field.send_keys(topic_text)

    search_button = driver.find_element('class name', 'teacher-lessons__search-button')
    search_button.click()
    
    lesson_name = driver.find_element('class name', 'teacher-lessons__lesson-name')

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(('class name', 'teacher-lessons__lesson-name'))
    )

    if lesson_name.text == topic_text:
        lesson_statis_button = driver.find_element('class name', 'teacher-lessons__lesson-stats')
        lesson_statis_button.click()
        time.sleep(1)
        
        try:
            lesson_stats_title = driver.find_element('class name', 'teacher-lesson-stat__title')
            assert True
        except:
            assert False
