import pytest
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
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

# Создание дисциплины
def test_create_discipline(test_true_login):
    driver = test_true_login 
    discipline_button = driver.find_element('xpath', '//*[@id="root"]/header/div/div[2]/div[1]/a[2]')
    discipline_button.click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(('xpath', '//*[@id="root"]/main/div/div[1]/a'))
    )

    create_discipline_button = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/a')
    create_discipline_button.click()

    discipline_input = driver.find_element("id", 'discipline')
    discipline_input.send_keys(text_discipline)

    apply_create_discipline_button = driver.find_element('xpath', '//*[@id="root"]/main/div[2]/div/div/button[1]')
    apply_create_discipline_button.click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(('xpath', '//*[text()="Дисциплина успешно добавлена!"]'))
        )

        toast_message = driver.find_element('xpath', '//*[text()="Дисциплина успешно добавлена!"]')
        
        WebDriverWait(driver, 10).until(
            EC.visibility_of(toast_message)
        )
        assert "Дисциплина успешно добавлена!" in toast_message.text
    except:
        assert False

# Поиск созданной дисциплины
def test_search_discipline(test_true_login):
    driver = test_true_login
    discipline_button = driver.find_element('xpath', '//*[@id="root"]/header/div/div[2]/div[1]/a[2]')
    discipline_button.click()

    discipline_search = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/form/input')
    discipline_search.send_keys(text_discipline)

    first_element = driver.find_element('xpath', '//*[@id="root"]/main/div/ul/li/div[1]/span')

    assert first_element.text == text_discipline
