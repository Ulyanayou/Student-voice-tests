import pytest
import time
import os
import pyperclip
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('URL')
username = os.getenv('USERNAME_TEACHER')
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

# Правильное заполнение формы обратной связи
def test_true_feedback_form(test_true_login):
    driver = test_true_login

    # Создание нового урока
    create_lesson_button = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/a')
    create_lesson_button.click()
    time.sleep(1)

    # Выбор института и дисциплины
    select_institute(driver)
    select_discipline(driver)

    # Заполнение формы урока
    fill_lesson_form(driver)

    # Применение и ожидание создания урока
    submit_lesson(driver)

    # Загрузка QR-кода
    download_qr_code(driver)

    # Перейти по скопированной ссылке
    copied_url = pyperclip.paste()
    driver.get(copied_url)

    # Заполнение формы отзыва
    fill_feedback_form(driver)

    # Проверка успешного отправления отзыва
    verify_feedback_submission(driver)


def select_institute(driver):
    institute_select = driver.find_element("id", 'institute')
    select = Select(institute_select)
    select.select_by_value('77')


def select_discipline(driver):
    select_element = driver.find_element('id', 'discipline')
    select = Select(select_element)
    select.select_by_visible_text(text_discipline)


def fill_lesson_form(driver):
    topic = driver.find_element('xpath', '//*[@id="topic"]')
    topic.send_keys(f'Введение в {text_discipline}')

    location = driver.find_element('xpath', '//*[@id="location"]')
    location.send_keys('Дистанционно')

    current_date = datetime.now().strftime('%d-%m-%Y')
    date_input = driver.find_element('id', 'date')
    date_input.send_keys(current_date)

    current_time = datetime.now()
    start_time = (current_time - timedelta(hours=0.1)).strftime('%H:%M')
    end_time = (current_time + timedelta(hours=0.2)).strftime('%H:%M')

    start_time_input = driver.find_element('id', 'startTime')
    start_time_input.send_keys(start_time)

    end_time_input = driver.find_element('id', 'endTime')
    end_time_input.send_keys(end_time)


def submit_lesson(driver):
    apply_create_lesson_button = driver.find_element('class name', 'teacher-lesson-create__submit-button')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    apply_create_lesson_button.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(('class name', 'teacher-lesson-create__qr-action-button'))
    )
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(('class name', 'teacher-lesson-create__qr-action-button'))
    )


def download_qr_code(driver):
    download_qr_button = driver.find_element('xpath', '//*[@id="root"]/main/div[2]/form/div[8]/div[2]/button[2]')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    download_qr_button.click()
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('xpath', '//*[text()="Ссылка скопирована в буфер обмена."]'))
    )

    toast_message = driver.find_element('xpath', '//*[text()="Ссылка скопирована в буфер обмена."]')

    WebDriverWait(driver, 10).until(
        EC.visibility_of(toast_message)
    )


def fill_feedback_form(driver):
    student_name_input = driver.find_element('class name', 'stud-form__input')
    student_name_input.send_keys('Васильев Василий Васильевич')

    stars = driver.find_elements('class name', 'stud-form__star')
    driver.execute_script("arguments[0].scrollIntoView();", stars[0])
    for star in stars:
        time.sleep(1)
        star.click()

    textarea = driver.find_element('class name', 'stud-form__textarea')
    textarea.send_keys('Всё очень понравилось!')

    submit_button = driver.find_element('class name', 'stud-form__submit-button')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    submit_button.click()


def verify_feedback_submission(driver):
    time.sleep(1)
    header = driver.find_element('tag name', 'h1')
    assert header.text == "Спасибо за отзыв! Вы улучшаете процесс обучения."
