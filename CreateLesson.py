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

# Создание пары
def test_create_lesson(test_true_login):
    driver = test_true_login 

    create_lesson_button = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/a')
    create_lesson_button.click()

    institute_select = driver.find_element("id", 'institute') 
    select = Select(institute_select)
    select.select_by_value('77')

    select_element = driver.find_element('id', 'discipline')
    select = Select(select_element)
    select.select_by_visible_text(text_discipline)

    topic = driver.find_element('xpath', '//*[@id="topic"]')
    topic.send_keys(f'Введение в {text_discipline}')

    location =  driver.find_element('xpath', '//*[@id="location"]')
    location.send_keys('Дистанционно')

    current_date = datetime.now().strftime('%d-%m-%Y')
    date_input = driver.find_element('id', 'date')
    date_input.send_keys(current_date)

    start_time_input = driver.find_element('id', 'startTime')
    start_time_input.send_keys('00:00')

    end_time_input = driver.find_element('id', 'endTime')
    end_time_input.send_keys('23:59')

    apply_create_lesson_button = driver.find_element('class name', 'teacher-lesson-create__submit-button')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    apply_create_lesson_button.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(('class name', 'teacher-lesson-create__submit-button'))
    )
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(('class name', 'teacher-lesson-create__submit-button'))
    )
    apply_button = driver.find_element('class name', 'teacher-lesson-create__submit-button')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    apply_button.click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(('xpath', '//*[text()="Данные урока обновлены."]'))
        )

        toast_message = driver.find_element('xpath', '//*[text()="Данные урока обновлены."]')
        
        WebDriverWait(driver, 10).until(
            EC.visibility_of(toast_message)
        )
        assert "Данные урока обновлены." in toast_message.text
    except:
        assert False
