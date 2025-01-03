import pytest
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Загрузка переменных окружения
url = os.getenv('URL')
username = os.getenv('USERNAME_TEACHER')
password = os.getenv('PASSWORD_TEACHER')
text_discipline = os.getenv('TEXT_DISCIPLINE')
topic_text = f'Введение в {text_discipline}'

@pytest.fixture
def test_true_login(setup_browser):
    driver = setup_browser

    # Логин в систему
    driver.get(url)
    login_field = driver.find_element('id', 'username')
    login_field.send_keys(username)
    
    password_field = driver.find_element('id', 'password')
    password_field.send_keys(password)
    
    login_button = driver.find_element('xpath', "//button[text()='Войти']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  
    login_button.click()

    # Ожидание появления нужной страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('xpath', "//h1[@class='teacher-lessons__main-container-title']"))
    )

    assert driver.current_url == url + 'teacher-lessons'
    return driver

def wait_for_element(driver, locator, timeout=10):
    """ Утилита для ожидания появления элемента. """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def create_lesson(driver):
    """ Функция для создания урока. """
    # Нажатие на кнопку создания урока
    create_lesson_button = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/a')
    create_lesson_button.click()
    time.sleep(1)

    # Выбор учебного заведения
    institute_select = driver.find_element("id", 'institute') 
    select = Select(institute_select)
    select.select_by_value('77')

    # Выбор дисциплины
    select_element = driver.find_element('id', 'discipline')
    select = Select(select_element)
    select.select_by_visible_text(text_discipline)

    # Заполнение темы, места проведения, даты и времени
    topic = driver.find_element('xpath', '//*[@id="topic"]')
    topic.send_keys(topic_text)
    
    location = driver.find_element('xpath', '//*[@id="location"]')
    location.send_keys('Дистанционно')

    current_date = datetime.now().strftime('%d-%m-%Y')
    date_input = driver.find_element('id', 'date')
    date_input.send_keys(current_date)

    start_time_input = driver.find_element('id', 'startTime')
    start_time_input.send_keys('01:00')

    end_time_input = driver.find_element('id', 'endTime')
    end_time_input.send_keys('23:00')

    # Нажатие на кнопку создания урока
    apply_create_lesson_button = driver.find_element('class name', 'teacher-lesson-create__submit-button')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    apply_create_lesson_button.click()

    # Ожидание кнопки "Применить"
    time.sleep(1)

    # Подтверждение создания урока
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    apply_button = driver.find_element('class name', 'teacher-lesson-create__submit-button')
    apply_button.click()

    # Ожидание успешного сообщения
    wait_for_element(driver, ('xpath', '//*[text()="Данные урока обновлены."]'))
    toast_message = driver.find_element('xpath', '//*[text()="Данные урока обновлены."]')
    wait_for_element(driver, ('xpath', '//*[text()="Данные урока обновлены."]'))
    
    # Возврат к списку уроков
    for _ in range(2):
        back_button = driver.find_element('class name', 'teacher-lesson-create__back-button')
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        back_button.click()

# Поиск пары
def test_search_lesson(test_true_login):
    driver = test_true_login

    # Создание урока
    create_lesson(driver)

    # Поиск урока по теме
    search_field = driver.find_element('class name', 'teacher-lessons__search-input')
    search_field.send_keys(topic_text)

    search_button = driver.find_element('class name', 'teacher-lessons__search-button')
    search_button.click()
    time.sleep(1)

    # Проверка наличия урока с нужной темой
    lesson_name = wait_for_element(driver, ('class name', 'teacher-lessons__lesson-name'))
    assert lesson_name.text == topic_text
