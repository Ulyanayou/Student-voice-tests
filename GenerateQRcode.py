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


@pytest.fixture
def test_true_login(setup_browser):
    driver = setup_browser
    driver.get(url)

    # Логин в систему
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


# Функция для заполнения формы создания урока
def fill_lesson_form(driver, topic_text):
    # Выбор учебного заведения
    institute_select = driver.find_element("id", 'institute')
    select = Select(institute_select)
    select.select_by_value('77')

    # Выбор дисциплины
    select_element = driver.find_element('id', 'discipline')
    select = Select(select_element)
    select.select_by_visible_text(text_discipline)

    # Заполнение темы урока
    topic = driver.find_element('xpath', '//*[@id="topic"]')
    topic.send_keys(topic_text)

    # Заполнение места проведения
    location = driver.find_element('xpath', '//*[@id="location"]')
    location.send_keys('Дистанционно')

    # Заполнение даты
    current_date = datetime.now().strftime('%d-%m-%Y')
    date_input = driver.find_element('id', 'date')
    date_input.send_keys(current_date)

    # Заполнение времени начала и окончания
    start_time_input = driver.find_element('id', 'startTime')
    start_time_input.send_keys('00:00')

    end_time_input = driver.find_element('id', 'endTime')
    end_time_input.send_keys('23:00')

    # Нажатие на кнопку "Создать урок"
    apply_create_lesson_button = driver.find_element('class name', 'teacher-lesson-create__submit-button')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    apply_create_lesson_button.click()


# Функция для ожидания всплывающего сообщения
def wait_for_toast(driver, message):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(('xpath', f'//*[text()="{message}"]'))
        )
        toast_message = driver.find_element('xpath', f'//*[text()="{message}"]')
        WebDriverWait(driver, 10).until(
            EC.visibility_of(toast_message)
        )
        assert message in toast_message.text
    except Exception as e:
        print(f"Error: {e}")
        assert False


# Скачивание QR кода
def test_download_qr_code(test_true_login):
    driver = test_true_login 
    create_lesson_button = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/a')
    create_lesson_button.click()
    time.sleep(1)

    fill_lesson_form(driver, f'Введение в {text_discipline}')

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(('class name', 'teacher-lesson-create__qr-action-button'))
    )
    download_qr_button = driver.find_element('class name', 'teacher-lesson-create__qr-action-button')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    download_qr_button.click()
    time.sleep(2)

    wait_for_toast(driver, "QR-код скачан.")


# Продление QR кода на 10 минут
def test_to_extend_10m(test_true_login):
    driver = test_true_login 
    create_lesson_button = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/a')
    create_lesson_button.click()
    time.sleep(1)

    fill_lesson_form(driver, f'Введение в {text_discipline}')

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(('class name', 'teacher-lesson-create__qr-action-button'))
    )
    extend_qr_button = driver.find_element('xpath', '//*[@id="root"]/main/div[2]/form/div[8]/div[2]/button[3]')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    extend_qr_button.click()
    time.sleep(2)

    new_end_time_input = driver.find_element('id', 'endTime')
    assert new_end_time_input.get_attribute('value') == '23:10'


# Копирование ссылки на QR код
def test_copy_url_to_qr_code(test_true_login):
    driver = test_true_login 
    create_lesson_button = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/a')
    create_lesson_button.click()
    time.sleep(1)

    fill_lesson_form(driver, f'Введение в {text_discipline}')

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(('class name', 'teacher-lesson-create__qr-action-button'))
    )
    copy_qr_button = driver.find_element('xpath', '//*[@id="root"]/main/div[2]/form/div[8]/div[2]/button[2]')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    copy_qr_button.click()
    time.sleep(2)

    wait_for_toast(driver, "Ссылка скопирована в буфер обмена.")

    

