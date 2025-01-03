import pytest
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('URL')
username = os.getenv('USERNAME_ADMIN')
password = os.getenv('PASSWORD_ADMIN')

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
        EC.presence_of_element_located(('xpath', "//h1[@class='admin-users__main-container-title']"))
    )

    assert driver.current_url == url + 'admin-users'
    return driver

# Выгрузка рейтинга в excel
def test_teacher_statistic(test_true_login):
    driver = test_true_login

    search_input = driver.find_element("class name", "admin-users__search-input")
    search_input.send_keys("Преподаватель")
    search_input.send_keys(Keys.RETURN)

    stats_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('class name', "admin-users__user-stats"))
    )

    stats_button.click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(('xpath', "//h1[text()='Статистика пользователя']"))
        )

        export_button = driver.find_element("class name", "admin-user-stat__export-btn")
        export_button.click()

        time.sleep(1)
        assert True
    except:
        assert False




